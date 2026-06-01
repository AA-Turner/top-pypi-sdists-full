"""Tests for v0.1.125 (#328) — scripts/extract_changelog_section.py.

The extractor pulls the CHANGELOG section for a given release tag so
the post-release-triage workflow can prepend a "What's new" block above
the deterministic triage output. Three behaviors covered:
1. Tag with `v` prefix and bare-version tag both find the section.
2. Last section in the file is captured to EOF (no trailing `## [`).
3. Missing tag returns an empty string (caller treats as fall-through).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts/extract_changelog_section.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("extract_changelog_section", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SAMPLE_CHANGELOG = """\
# Changelog

All notable changes loosely follow Keep a Changelog.

## [0.1.125] — 2026-05-15

**Sample release.** A short blurb about what shipped.

### Added

- One thing.
- Another thing.

## [0.1.124] — 2026-05-15

**Previous release.** Different content.

### Removed

- A flag.

## [0.1.0] — 2026-04-29

Initial release.
"""


def test_extract_with_v_prefix() -> None:
    mod = _load_module()
    section = mod.extract_section(SAMPLE_CHANGELOG, "v0.1.125")
    assert section.startswith("## [0.1.125] — 2026-05-15")
    assert "**Sample release.**" in section
    # Stops before the next release header.
    assert "## [0.1.124]" not in section


def test_extract_with_bare_version() -> None:
    mod = _load_module()
    section = mod.extract_section(SAMPLE_CHANGELOG, "0.1.125")
    assert "**Sample release.**" in section
    assert "## [0.1.124]" not in section


def test_extract_middle_section_stops_at_next_header() -> None:
    mod = _load_module()
    section = mod.extract_section(SAMPLE_CHANGELOG, "0.1.124")
    assert "**Previous release.**" in section
    assert "## [0.1.125]" not in section
    assert "## [0.1.0]" not in section


def test_extract_last_section_runs_to_eof() -> None:
    mod = _load_module()
    section = mod.extract_section(SAMPLE_CHANGELOG, "0.1.0")
    assert "Initial release." in section


def test_extract_missing_tag_returns_empty() -> None:
    mod = _load_module()
    section = mod.extract_section(SAMPLE_CHANGELOG, "9.9.9")
    assert section == ""


def test_extract_real_changelog_for_current_version() -> None:
    """Smoke-check the extractor against the real CHANGELOG.md.
    The current __version__ should always have a section.
    """
    mod = _load_module()
    real_changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    from efterlev import __version__

    section = mod.extract_section(real_changelog, __version__)
    assert section, f"no CHANGELOG section for current __version__={__version__}"
    assert section.startswith(f"## [{__version__}]")
