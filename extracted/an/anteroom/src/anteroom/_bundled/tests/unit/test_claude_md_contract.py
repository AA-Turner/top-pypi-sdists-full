"""Contract tests validating CLAUDE.md references resolve to real modules (#1180).

Parses all .py module references from CLAUDE.md and asserts each resolves
under src/anteroom/. Three extraction modes:
  (a) Slash-qualified backtick paths (e.g. `services/agent_loop.py`)
  (b) Bare backtick filenames in prose outside fenced code blocks
  (c) Bare filenames inside fenced code blocks (architecture diagram)
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"
_SRC_ROOT = _REPO_ROOT / "src" / "anteroom"

# Shell-command prefixes whose lines we skip entirely.
_SHELL_PREFIXES = (
    "pip install",
    "pip ",
    "pytest",
    "ruff ",
    "mypy ",
    "aroom",
    "npx ",
    "cd ",
    "make ",
    "invoke ",
    "docker ",
    "source ",
    "python",
    ".venv/",
    "gh ",
    "twine ",
    "git ",
)

# Filenames that are not Python modules (config, data files, etc.).
_NON_MODULE_NAMES = frozenset(
    {
        "config.yaml",
        "team.yaml",
        "pack.yaml",
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "conftest.py",
        "index.html",
    }
)

# Glob-like patterns to skip (e.g. *.py in prose about patterns).
_GLOB_PATTERN = re.compile(r"^\*\.")


def _is_shell_line(line: str) -> bool:
    stripped = line.strip()
    return any(stripped.startswith(p) for p in _SHELL_PREFIXES)


def _split_fenced_blocks(text: str) -> tuple[list[str], list[str]]:
    """Split CLAUDE.md into prose lines and fenced-code-block lines."""
    prose_lines: list[str] = []
    code_lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            code_lines.append(line)
        else:
            prose_lines.append(line)
    return prose_lines, code_lines


def _extract_qualified_backtick_paths(lines: list[str]) -> set[str]:
    """Mode (a): backtick-quoted strings containing '/' and ending in .py."""
    paths: set[str] = set()
    for line in lines:
        if _is_shell_line(line):
            continue
        for m in re.finditer(r"`([^`]*?/[^`]*?\.py)`", line):
            paths.add(m.group(1))
    return paths


def _extract_bare_backtick_filenames(lines: list[str]) -> set[str]:
    """Mode (b): backtick-quoted *.py without '/' in prose (not code blocks)."""
    names: set[str] = set()
    for line in lines:
        if _is_shell_line(line):
            continue
        for m in re.finditer(r"`([A-Za-z_][A-Za-z0-9_]*\.py)`", line):
            name = m.group(1)
            if name not in _NON_MODULE_NAMES and not _GLOB_PATTERN.match(name):
                names.add(name)
    return names


def _extract_bare_code_block_filenames(lines: list[str]) -> set[str]:
    """Mode (c): bare *.py tokens inside fenced code blocks."""
    names: set[str] = set()
    for line in lines:
        if _is_shell_line(line):
            continue
        for m in re.finditer(r"\b([A-Za-z_][A-Za-z0-9_]*\.py)\b", line):
            name = m.group(1)
            if name not in _NON_MODULE_NAMES and not _GLOB_PATTERN.match(name):
                names.add(name)
    return names


# Paths that resolve against repo root instead of src/anteroom/.
_REPO_ROOT_PREFIXES = ("tests/", "docs/", "evals/", "demos/", "scripts/", "examples/")


def _resolve_qualified(path: str) -> bool:
    """Check if a slash-qualified path resolves under src/anteroom/ or repo root."""
    if any(path.startswith(p) for p in _REPO_ROOT_PREFIXES):
        return (_REPO_ROOT / path).is_file()
    return (_SRC_ROOT / path).is_file()


def _resolve_bare(filename: str) -> bool:
    """Check if a bare filename exists anywhere under src/anteroom/."""
    return any(True for _ in _SRC_ROOT.rglob(filename))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def claude_md_text() -> str:
    return _CLAUDE_MD.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def prose_lines(claude_md_text: str) -> list[str]:
    prose, _ = _split_fenced_blocks(claude_md_text)
    return prose


@pytest.fixture(scope="module")
def code_lines(claude_md_text: str) -> list[str]:
    _, code = _split_fenced_blocks(claude_md_text)
    return code


# ---------------------------------------------------------------------------
# Contract tests
# ---------------------------------------------------------------------------


class TestQualifiedPyPaths:
    """Every slash-qualified .py backtick reference in CLAUDE.md must resolve."""

    def test_qualified_py_paths_exist(self, prose_lines: list[str], code_lines: list[str]) -> None:
        paths = _extract_qualified_backtick_paths(prose_lines) | _extract_qualified_backtick_paths(code_lines)
        assert paths, "Parser found no qualified paths — check extraction logic"
        missing = sorted(p for p in paths if not _resolve_qualified(p))
        assert not missing, "CLAUDE.md references .py paths that do not exist under src/anteroom/:\n" + "\n".join(
            f"  - {p}" for p in missing
        )


class TestBarePyFilenames:
    """Every bare .py backtick filename in CLAUDE.md must exist somewhere in the package."""

    def test_bare_py_filenames_exist(self, prose_lines: list[str], code_lines: list[str]) -> None:
        names = _extract_bare_backtick_filenames(prose_lines) | _extract_bare_code_block_filenames(code_lines)
        assert names, "Parser found no bare filenames — check extraction logic"
        missing = sorted(n for n in names if not _resolve_bare(n))
        assert not missing, "CLAUDE.md references .py filenames not found under src/anteroom/:\n" + "\n".join(
            f"  - {n}" for n in missing
        )


class TestParserExtractionCorrectness:
    """Self-tests to prevent parser degradation."""

    def test_extracts_known_qualified_path(self) -> None:
        lines = ["- **`services/agent_loop.py`** — the agent loop"]
        result = _extract_qualified_backtick_paths(lines)
        assert "services/agent_loop.py" in result

    def test_extracts_known_bare_backtick(self) -> None:
        lines = ["Translates to the Anthropic API and back via `ai_service.py`."]
        result = _extract_bare_backtick_filenames(lines)
        assert "ai_service.py" in result

    def test_extracts_known_code_block_filename(self) -> None:
        lines = ["  agent_turn.py          storage.py → SQLite"]
        result = _extract_bare_code_block_filenames(lines)
        assert "storage.py" in result

    def test_skips_shell_commands(self) -> None:
        lines = ["pip install anteroom[dev]", "pytest tests/unit/test_foo.py -v"]
        assert not _extract_qualified_backtick_paths(lines)
        assert not _extract_bare_backtick_filenames(lines)
        assert not _extract_bare_code_block_filenames(lines)

    def test_skips_non_module_names(self) -> None:
        lines = ["`config.yaml` is the main config file"]
        assert not _extract_bare_backtick_filenames(lines)

    def test_skips_glob_patterns(self) -> None:
        code = ["*.py files in the glob pattern"]
        assert not _extract_bare_code_block_filenames(code)
