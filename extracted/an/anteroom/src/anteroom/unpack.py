"""Extract bundled auxiliary files (tests, docs, evals, etc.) to a directory.

Used for offline development on machines that can only ``pip install anteroom[kitchensink]``.
"""

from __future__ import annotations

import shutil
import sys
from collections.abc import Callable
from pathlib import Path

_BUNDLED_ITEMS = [
    "tests",
    "docs",
    "evals",
    "demos",
    "examples",
    "scripts",
    "pyproject.toml",
    "mkdocs.yml",
    "codecov.yml",
    "vitest.config.js",
    "README.md",
    "VISION.md",
    "SECURITY.md",
    "CLAUDE.md",
    "ROADMAP.md",
    "LICENSE",
    ".readthedocs.yaml",
    ".semgrepignore",
]


def _bundled_root() -> Path:
    """Return the path to the _bundled directory inside the installed package."""
    return Path(__file__).resolve().parent / "_bundled"


def _make_ignore_fn(bundled_root: Path) -> Callable[[str, list[str]], set[str]]:
    """Return an ignore function for copytree that skips junk and out-of-tree symlinks."""
    resolved_root = bundled_root.resolve()

    def _ignore(directory: str, entries: list[str]) -> set[str]:
        ignored: set[str] = set()
        for entry in entries:
            if entry in ("__pycache__", "node_modules", ".pytest_cache"):
                ignored.add(entry)
                continue
            full = Path(directory) / entry
            if full.is_symlink():
                target = full.resolve()
                if not target.exists():
                    ignored.add(entry)
                elif not target.is_relative_to(resolved_root):
                    ignored.add(entry)
        return ignored

    return _ignore


def unpack(dest: str | Path, *, force: bool = False) -> None:
    """Copy bundled files to *dest*, recreating the original repo layout."""
    dest = Path(dest)
    bundled = _bundled_root()

    if not bundled.is_dir():
        print("Error: bundled data not found in this installation.", file=sys.stderr)
        print("Was anteroom installed from a wheel that includes _bundled/?", file=sys.stderr)
        sys.exit(1)

    if dest.exists() and not force:
        print(f"Error: destination already exists: {dest}", file=sys.stderr)
        print("Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    dest.mkdir(parents=True, exist_ok=True)
    ignore_fn = _make_ignore_fn(bundled)

    copied = 0
    for item_name in _BUNDLED_ITEMS:
        src = bundled / item_name
        dst = dest / item_name
        if not src.exists():
            continue
        if src.is_dir():
            if dst.exists() and force:
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=ignore_fn, dirs_exist_ok=force)
        else:
            shutil.copy2(src, dst)
        copied += 1

    # Copy (not symlink) the package source so the unpacked tree is self-contained
    anteroom_pkg = Path(__file__).resolve().parent
    src_dir = dest / "src" / "anteroom"
    if not src_dir.exists():
        src_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            anteroom_pkg,
            src_dir,
            ignore=shutil.ignore_patterns("__pycache__", "_bundled", "*.pyc"),
        )

    from .services.docs_project_links import render_project_links_in_place

    render_project_links_in_place(dest)

    print(f"Unpacked {copied} items to {dest.resolve()}")
    print()
    print("Quick start:")
    print(f"  cd {dest}")
    print("  pytest tests/unit/ -v")
    print("  ruff check src/ tests/")
