#!/usr/bin/env python3
"""Migrate mistralai_workflows -> mistralai.workflows (PEP 420 namespace package).

This script performs the full namespace migration:
1. Moves directory structure: mistralai_workflows/ -> mistralai/workflows/
2. Rewrites Python imports in all .py files
3. Updates pyproject.toml, tasks.py, CI configs, scripts, docs
4. Ensures PEP 420 compliance (no __init__.py at namespace levels)
5. Moves plugin directory structures similarly

Run from workflow_sdk/:
    python scripts/migrate_namespace.py [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

OLD_PKG = "mistralai_workflows"
NEW_PKG = "mistralai.workflows"
NEW_PKG_PATH = "mistralai/workflows"

# Directories relative to SDK root that should NOT have __init__.py (PEP 420 namespace levels)
PEP420_NAMESPACE_DIRS: list[str] = [
    "mistralai",
    "mistralai/workflows/plugins",
    "plugins/mistralai/mistralai",
    "plugins/mistralai/mistralai/workflows/plugins",
    "plugins/webhook/mistralai",
    "plugins/webhook/mistralai/workflows/plugins",
    "plugins/nuage_v2/mistralai",
    "plugins/nuage_v2/mistralai/workflows/plugins",
]

GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
NC = "\033[0m"


def log_action(msg: str) -> None:
    print(f"  {GREEN}>{NC} {msg}")


def log_warn(msg: str) -> None:
    print(f"  {YELLOW}!{NC} {msg}")


def log_error(msg: str) -> None:
    print(f"  {RED}x{NC} {msg}")


# ---------------------------------------------------------------------------
# Step 1: Move directories
# ---------------------------------------------------------------------------

def _has_source_files(path: Path) -> bool:
    """Check if a directory tree contains any non-cache source files."""
    for root, _dirs, files in os.walk(path):
        for f in files:
            if not f.endswith(".pyc"):
                return True
    return False


def move_directory(sdk_root: Path, src: str, dst: str, *, dry_run: bool) -> None:
    """Move src directory to dst, creating parent dirs as needed.

    If dst already exists but contains only __pycache__ (stale bytecode from
    a previous editable install), it is removed first so the move can proceed.
    """
    src_path = sdk_root / src
    dst_path = sdk_root / dst

    if not src_path.exists():
        log_warn(f"Source {src} does not exist, skipping")
        return

    if dst_path.exists():
        if _has_source_files(dst_path):
            log_warn(f"Destination {dst} already exists with source files, skipping move")
            return
        # Only stale __pycache__ — safe to remove
        log_action(f"Removing stale {dst} (only __pycache__)")
        if not dry_run:
            shutil.rmtree(dst_path)

    log_action(f"mv {src} -> {dst}")
    if not dry_run:
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dst_path))


def move_directories(sdk_root: Path, *, dry_run: bool) -> None:
    """Move all mistralai_workflows/ directories to mistralai/workflows/."""
    print("\n[1] Moving directory structures")

    # Core package
    move_directory(sdk_root, "mistralai_workflows", "mistralai/workflows", dry_run=dry_run)

    # Plugin namespace directories
    for plugin in ["mistralai", "webhook", "nuage_v2"]:
        plugin_old = f"plugins/{plugin}/mistralai_workflows"
        plugin_new = f"plugins/{plugin}/mistralai/workflows"
        move_directory(sdk_root, plugin_old, plugin_new, dry_run=dry_run)


# ---------------------------------------------------------------------------
# Step 2: Rewrite Python imports in .py files
# ---------------------------------------------------------------------------

def rewrite_python_imports(content: str) -> str:
    """Rewrite all mistralai_workflows references to mistralai.workflows in Python source.

    Import patterns handled:
      1. ``import mistralai_workflows``
         -> ``import mistralai.workflows as mistralai_workflows``
         This preserves call-sites like ``mistralai_workflows.execute_workflow(...)``
         which would break if the binding name changed to a dotted namespace
         (PEP 420 namespace packages don't support attribute-chain resolution
         inside Temporal's workflow sandbox).

      2. ``import mistralai_workflows as <alias>``
         -> ``import mistralai.workflows as <alias>``

      3. ``import mistralai_workflows.<sub> as <alias>``
         -> ``import mistralai.workflows.<sub> as <alias>``

      4. ``from mistralai_workflows import ...`` / ``from mistralai_workflows.<sub> import ...``
         -> ``from mistralai.workflows import ...`` / ``from mistralai.workflows.<sub> import ...``

      5. Any other occurrence (strings, comments, etc.)
         -> simple text replacement
    """
    # Pattern 1: bare ``import mistralai_workflows`` (no alias, no sub-module)
    #   -> ``import mistralai.workflows as mistralai_workflows``
    #   Call-sites like ``mistralai_workflows.execute_workflow(...)`` keep working
    #   because the alias preserves the original binding name.
    #   We must NOT replace ``mistralai_workflows`` in these call-sites.
    has_bare_import = bool(re.search(r"^\s*import mistralai_workflows\s*$", content, re.MULTILINE))

    content = re.sub(
        r"^(\s*)import mistralai_workflows(\s*$)",
        r"\1import mistralai.workflows as mistralai_workflows\2",
        content,
        flags=re.MULTILINE,
    )

    # Pattern 2: ``from mistralai_workflows`` -> ``from mistralai.workflows``
    content = re.sub(
        r"^(\s*from\s+)mistralai_workflows",
        r"\1mistralai.workflows",
        content,
        flags=re.MULTILINE,
    )

    # Pattern 3: ``import mistralai_workflows.X as Y`` or ``import mistralai_workflows as Y``
    #   (already-aliased imports -- NOT the bare import we handled above)
    content = re.sub(
        r"^(import\s+)mistralai_workflows(\.\S+\s+as\s+)",
        r"\1mistralai.workflows\2",
        content,
        flags=re.MULTILINE,
    )
    content = re.sub(
        r"^(import\s+)mistralai_workflows(\s+as\s+)",
        r"\1mistralai.workflows\2",
        content,
        flags=re.MULTILINE,
    )

    # Replace occurrences inside string literals (e.g. mock.patch targets).
    # These are module paths that must be migrated regardless of bare imports.
    content = re.sub(
        r"""(["'])mistralai_workflows\b""",
        r"\1mistralai.workflows",
        content,
    )

    if not has_bare_import:
        # No bare import -> safe to replace all remaining occurrences
        # (e.g. in comments, type annotations, other non-identifier contexts)
        content = content.replace("mistralai_workflows", "mistralai.workflows")

    return content


def rewrite_py_files(sdk_root: Path, *, dry_run: bool) -> int:
    """Rewrite imports in all .py files under sdk_root."""
    print("\n[2] Rewriting Python imports")

    count = 0
    for root, dirs, files in os.walk(sdk_root):
        # Skip .venv, __pycache__, .git, node_modules
        dirs[:] = [
            d for d in dirs
            if d not in {".venv", "__pycache__", ".git", "node_modules", ".mypy_cache", ".pytest_cache", ".ruff_cache", "scripts"}
        ]

        # Files handled by dedicated steps (tasks.py -> step 4)
        SKIP_FILES = {"tasks.py"}

        for fname in files:
            if not fname.endswith(".py") or fname in SKIP_FILES:
                continue

            fpath = Path(root) / fname
            try:
                original = fpath.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue

            if OLD_PKG not in original:
                continue

            updated = rewrite_python_imports(original)
            if updated != original:
                count += 1
                rel = fpath.relative_to(sdk_root)
                log_action(f"Rewriting {rel}")
                if not dry_run:
                    fpath.write_text(updated, encoding="utf-8")

    log_action(f"Rewrote {count} Python file(s)")
    return count


# ---------------------------------------------------------------------------
# Step 3: Update pyproject.toml files
# ---------------------------------------------------------------------------

def rewrite_toml_file(fpath: Path, *, dry_run: bool) -> bool:
    """Rewrite mistralai_workflows references in a TOML file."""
    if not fpath.exists():
        return False

    original = fpath.read_text(encoding="utf-8")
    if OLD_PKG not in original:
        return False

    updated = original

    # packages = ["mistralai_workflows"] -> packages = ["mistralai"]
    updated = updated.replace(
        'packages = ["mistralai_workflows"]',
        'packages = ["mistralai"]',
    )

    # exclude = ["mistralai_workflows/__init__.py"]
    # -> exclude = ["mistralai/__init__.py", "mistralai/workflows/__init__.py", "mistralai/workflows/plugins/__init__.py"]
    updated = updated.replace(
        'exclude = ["mistralai_workflows/__init__.py"]',
        'exclude = ["mistralai/__init__.py", "mistralai/workflows/__init__.py", "mistralai/workflows/plugins/__init__.py"]',
    )

    # known-first-party references
    updated = updated.replace(
        '"mistralai_workflows"',
        '"mistralai.workflows"',
    )

    # General fallback for any remaining references (module paths in mypy overrides, etc.)
    updated = updated.replace("mistralai_workflows", "mistralai.workflows")

    # Ensure mypy namespace package settings are present for PEP 420 resolution
    if "namespace_packages" not in updated and "[tool.mypy]" in updated:
        updated = updated.replace(
            'plugins = ["pydantic.mypy"]',
            'plugins = ["pydantic.mypy"]\nnamespace_packages = true\nexplicit_package_bases = true\nmypy_path = "."',
        )

    if updated != original:
        log_action(f"Updating {fpath.name}")
        if not dry_run:
            fpath.write_text(updated, encoding="utf-8")
        return True
    return False


def update_pyproject_files(sdk_root: Path, *, dry_run: bool) -> None:
    """Update all pyproject.toml files."""
    print("\n[3] Updating pyproject.toml files")

    # Root pyproject.toml
    rewrite_toml_file(sdk_root / "pyproject.toml", dry_run=dry_run)

    # Plugin pyproject.toml files
    for plugin in ["mistralai", "webhook", "nuage_v2"]:
        rewrite_toml_file(sdk_root / "plugins" / plugin / "pyproject.toml", dry_run=dry_run)


# ---------------------------------------------------------------------------
# Step 4: Update tasks.py
# ---------------------------------------------------------------------------

def _rewrite_tasks_file(fpath: Path, *, dry_run: bool) -> bool:
    """Rewrite a tasks.py file with path-aware logic.

    tasks.py files mix filesystem paths (``mistralai_workflows/``) and Python
    module names (``mistralai_workflows``).  A blanket text replace would turn
    paths into dotted names, so we handle each form explicitly:
      - ``mistralai_workflows/`` (path)  -> ``mistralai/workflows/``
      - ``mistralai_workflows``  (module) -> ``mistralai.workflows``
    """
    if not fpath.exists():
        return False

    original = fpath.read_text(encoding="utf-8")
    if OLD_PKG not in original:
        return False

    updated = original

    # Filesystem paths first (before the general module replace)
    updated = updated.replace("mistralai_workflows/", "mistralai/workflows/")

    # Module names (e.g. griffe check argument)
    updated = updated.replace("mistralai_workflows", "mistralai.workflows")

    if updated != original:
        rel = fpath.relative_to(fpath.parent.parent) if "plugins" in str(fpath) else Path(fpath.name)
        log_action(f"Rewriting {rel}")
        if not dry_run:
            fpath.write_text(updated, encoding="utf-8")
        return True
    return False


def update_tasks_files(sdk_root: Path, *, dry_run: bool) -> None:
    """Update all tasks.py files (root + plugins)."""
    print("\n[4] Updating tasks.py files")

    _rewrite_tasks_file(sdk_root / "tasks.py", dry_run=dry_run)
    for plugin in ["mistralai", "webhook", "nuage_v2"]:
        _rewrite_tasks_file(sdk_root / "plugins" / plugin / "tasks.py", dry_run=dry_run)


# ---------------------------------------------------------------------------
# Step 5: Update scripts
# ---------------------------------------------------------------------------

def update_scripts(sdk_root: Path, *, dry_run: bool) -> None:
    """Update script files that reference the old package name."""
    print("\n[5] Updating scripts")

    # check_public_api.py
    check_api = sdk_root / "scripts" / "check_public_api.py"
    if check_api.exists():
        original = check_api.read_text(encoding="utf-8")
        updated = original.replace(
            "workflow_sdk/mistralai_workflows/exports.py",
            "workflow_sdk/mistralai/workflows/exports.py",
        )
        updated = updated.replace("mistralai_workflows", "mistralai.workflows")
        if updated != original:
            log_action("Rewriting check_public_api.py")
            if not dry_run:
                check_api.write_text(updated, encoding="utf-8")

    # test_plugin_installs.sh
    test_plugins = sdk_root / "scripts" / "test_plugin_installs.sh"
    if test_plugins.exists():
        original = test_plugins.read_text(encoding="utf-8")
        updated = original.replace("mistralai_workflows", "mistralai.workflows")
        if updated != original:
            log_action("Rewriting test_plugin_installs.sh")
            if not dry_run:
                test_plugins.write_text(updated, encoding="utf-8")


# ---------------------------------------------------------------------------
# Step 6: Update all remaining text files (.md, .sh, .rst, .txt, .cfg)
# ---------------------------------------------------------------------------

TEXT_EXTENSIONS = {".md", ".sh", ".rst", ".txt", ".cfg"}
SKIP_DIRS = {".venv", "__pycache__", ".git", "node_modules", ".mypy_cache", ".pytest_cache", ".ruff_cache", "dist", ".eggs", "scripts"}


def update_text_files(sdk_root: Path, *, dry_run: bool) -> None:
    """Sweep all non-Python text files for stale references."""
    print("\n[6] Updating remaining text files (.md, .sh, etc.)")

    count = 0
    for root, dirs, files in os.walk(sdk_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if not any(fname.endswith(ext) for ext in TEXT_EXTENSIONS):
                continue

            fpath = Path(root) / fname
            try:
                original = fpath.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue

            if OLD_PKG not in original:
                continue

            # For paths (e.g. in shell scripts, CI, directory references) convert slash form first
            updated = original.replace("mistralai_workflows/", "mistralai/workflows/")
            # Then convert remaining dotted-module references
            updated = updated.replace("mistralai_workflows", "mistralai.workflows")

            if updated != original:
                count += 1
                rel = fpath.relative_to(sdk_root)
                log_action(f"Rewriting {rel}")
                if not dry_run:
                    fpath.write_text(updated, encoding="utf-8")

    log_action(f"Rewrote {count} text file(s)")


# ---------------------------------------------------------------------------
# Step 7: Update CI files
# ---------------------------------------------------------------------------

def update_ci_files(sdk_root: Path, *, dry_run: bool) -> None:
    """Update GitHub Actions workflow files."""
    print("\n[7] Updating CI workflow files")

    # The repo root is one level up from sdk_root
    repo_root = sdk_root.parent
    ci_dir = repo_root / ".github" / "workflows"

    if not ci_dir.exists():
        log_warn(".github/workflows not found")
        return

    for yaml_file in ci_dir.glob("*.yaml"):
        original = yaml_file.read_text(encoding="utf-8")
        if OLD_PKG not in original:
            continue

        # Update path filters: workflow_sdk/mistralai_workflows/** -> workflow_sdk/mistralai/workflows/**
        updated = original.replace("mistralai_workflows/", "mistralai/workflows/")
        # Also catch any dotted references
        updated = updated.replace("mistralai_workflows", "mistralai.workflows")

        if updated != original:
            log_action(f"Rewriting {yaml_file.relative_to(repo_root)}")
            if not dry_run:
                yaml_file.write_text(updated, encoding="utf-8")

    for yml_file in ci_dir.glob("*.yml"):
        original = yml_file.read_text(encoding="utf-8")
        if OLD_PKG not in original:
            continue

        updated = original.replace("mistralai_workflows/", "mistralai/workflows/")
        updated = updated.replace("mistralai_workflows", "mistralai.workflows")

        if updated != original:
            log_action(f"Rewriting {yml_file.relative_to(repo_root)}")
            if not dry_run:
                yml_file.write_text(updated, encoding="utf-8")


# ---------------------------------------------------------------------------
# Step 8: Enforce PEP 420 namespace compliance
# ---------------------------------------------------------------------------

def enforce_pep420(sdk_root: Path, *, dry_run: bool) -> None:
    """Remove __init__.py from PEP 420 namespace directories."""
    print("\n[8] Enforcing PEP 420 namespace compliance")

    for rel_dir in PEP420_NAMESPACE_DIRS:
        init_path = sdk_root / rel_dir / "__init__.py"
        if init_path.exists():
            log_action(f"Removing {rel_dir}/__init__.py (PEP 420 namespace)")
            if not dry_run:
                init_path.unlink()
        else:
            log_action(f"{rel_dir}/__init__.py absent (OK)")


# ---------------------------------------------------------------------------
# Step 9: Update __init__.py content
# ---------------------------------------------------------------------------

def update_init_files(sdk_root: Path, *, dry_run: bool) -> None:
    """Update __init__.py files that reference the old package name."""
    print("\n[9] Updating __init__.py content")

    # Core __init__.py
    core_init = sdk_root / "mistralai" / "workflows" / "__init__.py"
    if core_init.exists():
        original = core_init.read_text(encoding="utf-8")
        if OLD_PKG in original:
            updated = rewrite_python_imports(original)
            if updated != original:
                log_action("Rewriting mistralai/workflows/__init__.py")
                if not dry_run:
                    core_init.write_text(updated, encoding="utf-8")

    # Plugin __init__.py files
    for plugin in ["mistralai", "webhook", "nuage_v2"]:
        init_path = sdk_root / "plugins" / plugin / "mistralai" / "workflows" / "__init__.py"
        if init_path.exists():
            original = init_path.read_text(encoding="utf-8")
            if OLD_PKG in original:
                updated = rewrite_python_imports(original)
                if updated != original:
                    log_action(f"Rewriting plugins/{plugin}/mistralai/workflows/__init__.py")
                    if not dry_run:
                        init_path.write_text(updated, encoding="utf-8")


# ---------------------------------------------------------------------------
# Step 10: Verify no stale references remain
# ---------------------------------------------------------------------------

def _is_identifier_usage(line: str) -> bool:
    """Return True if every occurrence of ``mistralai_workflows`` on *line*
    is used as a Python identifier (e.g. alias or variable reference) rather
    than as a module/package path that should have been migrated.

    Stale module paths look like:
        import mistralai_workflows
        from mistralai_workflows.core import ...
        packages = ["mistralai_workflows"]

    Legitimate identifier usage (post-migration) looks like:
        import mistralai.workflows as mistralai_workflows
        mistralai_workflows.execute_workflow(...)
        mistralai_workflows.__path__ = ...
    """
    # If the line contains ``as mistralai_workflows`` it's an alias declaration
    # and any other ``mistralai_workflows`` on the same line is usage of that alias.
    if re.search(r"\bas\s+mistralai_workflows\b", line):
        return True
    # If mistralai_workflows is only used as a standalone identifier (not part of
    # a dotted import path like ``from mistralai_workflows.X``), it's fine.
    # Check: does it appear as ``from mistralai_workflows`` or ``import mistralai_workflows``
    # without an ``as`` alias already handled above?
    if re.search(r"\b(from|import)\s+mistralai_workflows\b", line):
        return False
    # Any remaining occurrence (e.g. ``mistralai_workflows.execute_workflow(...)``)
    # is a runtime reference to the alias — that's expected.
    return True


def verify_no_stale_references(sdk_root: Path) -> int:
    """Scan for any remaining mistralai_workflows references."""
    print("\n[10] Verifying no stale references remain")

    stale: list[tuple[Path, int, str]] = []

    for root, dirs, files in os.walk(sdk_root):
        dirs[:] = [
            d for d in dirs
            if d not in {".venv", "__pycache__", ".git", "node_modules", ".mypy_cache", ".pytest_cache", ".ruff_cache", "dist", ".eggs", "scripts"}
        ]

        for fname in files:
            # Check .py, .toml, .yaml, .yml, .sh, .md files
            if not any(fname.endswith(ext) for ext in (".py", ".toml", ".yaml", ".yml", ".sh", ".md", ".cfg")):
                continue

            fpath = Path(root) / fname
            try:
                content = fpath.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue

            for lineno, line in enumerate(content.splitlines(), 1):
                if OLD_PKG not in line:
                    continue
                # Skip this migration script itself
                if fpath.name == "migrate_namespace.py":
                    continue
                # After migration, mistralai_workflows is expected as a Python
                # identifier (alias from ``import mistralai.workflows as mistralai_workflows``
                # and its usage sites).  Only flag lines where it appears as a
                # *module path* -- i.e. ``import mistralai_workflows``,
                # ``from mistralai_workflows``, or a dotted path like
                # ``mistralai_workflows.plugins`` that isn't preceded by ``as ``.
                stripped = line.strip()
                if _is_identifier_usage(stripped):
                    continue
                stale.append((fpath, lineno, stripped))

    # Also check CI files in the repo root
    repo_root = sdk_root.parent
    ci_dir = repo_root / ".github" / "workflows"
    if ci_dir.exists():
        for yaml_file in list(ci_dir.glob("*.yaml")) + list(ci_dir.glob("*.yml")):
            try:
                content = yaml_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue
            for lineno, line in enumerate(content.splitlines(), 1):
                if OLD_PKG in line:
                    stale.append((yaml_file, lineno, line.strip()))

    if stale:
        log_error(f"Found {len(stale)} stale reference(s):")
        for fpath, lineno, line in stale[:30]:
            try:
                rel = fpath.relative_to(sdk_root)
            except ValueError:
                rel = fpath
            print(f"      {rel}:{lineno}: {line}")
        if len(stale) > 30:
            print(f"      ... and {len(stale) - 30} more")
        return len(stale)
    else:
        log_action("No stale references found")
        return 0


# ---------------------------------------------------------------------------
# Step 11: Migrate abraxas/ imports
# ---------------------------------------------------------------------------

SIBLING_TEXT_EXTENSIONS = {".md", ".mdx", ".sh", ".rst", ".txt", ".cfg"}


def _rewrite_sibling_text_file(fpath: Path, sibling_root: Path, name: str, *, dry_run: bool) -> bool:
    """Rewrite a non-Python file in a sibling directory, handling mixed path/module contexts.

    Docker-compose files contain both filesystem paths (``mistralai_workflows/``)
    and Python module names (``-m mistralai_workflows.examples``).
    """
    try:
        original = fpath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        return False

    if OLD_PKG not in original:
        return False

    # Filesystem paths first
    updated = original.replace("mistralai_workflows/", "mistralai/workflows/")
    # Then module names
    updated = updated.replace("mistralai_workflows", "mistralai.workflows")

    if updated != original:
        rel = fpath.relative_to(sibling_root)
        log_action(f"Rewriting {name}/{rel}")
        if not dry_run:
            fpath.write_text(updated, encoding="utf-8")
        return True
    return False


def update_sibling_directory(sibling_root: Path, name: str, step: int, *, dry_run: bool) -> None:
    """Rewrite mistralai_workflows imports in a sibling directory."""
    print(f"\n[{step}] Migrating {name}/ imports")

    py_count = 0
    text_count = 0

    for root, dirs, files in os.walk(sibling_root):
        dirs[:] = [
            d for d in dirs
            if d not in {".venv", "__pycache__", ".git", "node_modules", ".mypy_cache",
                         ".pytest_cache", ".ruff_cache", "dist", ".eggs", "scripts"}
        ]

        for fname in files:
            fpath = Path(root) / fname

            if fname.endswith(".py"):
                try:
                    original = fpath.read_text(encoding="utf-8")
                except (UnicodeDecodeError, PermissionError):
                    continue
                if OLD_PKG not in original:
                    continue
                updated = rewrite_python_imports(original)
                if updated != original:
                    py_count += 1
                    rel = fpath.relative_to(sibling_root)
                    log_action(f"Rewriting {name}/{rel}")
                    if not dry_run:
                        fpath.write_text(updated, encoding="utf-8")

            elif any(fname.endswith(ext) for ext in SIBLING_TEXT_EXTENSIONS):
                if _rewrite_sibling_text_file(fpath, sibling_root, name, dry_run=dry_run):
                    text_count += 1

            elif fname.endswith((".yaml", ".yml")):
                if _rewrite_sibling_text_file(fpath, sibling_root, name, dry_run=dry_run):
                    text_count += 1

    log_action(f"Rewrote {py_count} Python file(s) and {text_count} text file(s) in {name}/")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate mistralai_workflows -> mistralai.workflows (PEP 420 namespace)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without making changes",
    )
    parser.add_argument(
        "--sdk-root",
        type=Path,
        default=None,
        help="Path to workflow_sdk/ (default: auto-detect from script location)",
    )
    args = parser.parse_args()

    sdk_root = args.sdk_root or Path(__file__).resolve().parent.parent
    sdk_root = sdk_root.resolve()

    if not (sdk_root / "pyproject.toml").exists():
        log_error(f"Could not find pyproject.toml in {sdk_root}")
        return 1

    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"\nNamespace migration: {OLD_PKG} -> {NEW_PKG} [{mode}]")
    print(f"SDK root: {sdk_root}")

    # Execute migration steps in order
    move_directories(sdk_root, dry_run=args.dry_run)
    rewrite_py_files(sdk_root, dry_run=args.dry_run)
    update_pyproject_files(sdk_root, dry_run=args.dry_run)
    update_tasks_files(sdk_root, dry_run=args.dry_run)
    update_scripts(sdk_root, dry_run=args.dry_run)
    update_text_files(sdk_root, dry_run=args.dry_run)
    update_ci_files(sdk_root, dry_run=args.dry_run)
    enforce_pep420(sdk_root, dry_run=args.dry_run)
    update_init_files(sdk_root, dry_run=args.dry_run)

    # Migrate sibling directories (import rewrites + text files only)
    step = 11
    for sibling in ["abraxas"]:
        sibling_root = sdk_root.parent / sibling
        if sibling_root.is_dir():
            update_sibling_directory(sibling_root, sibling, step, dry_run=args.dry_run)
            step += 1

    if not args.dry_run:
        stale_count = verify_no_stale_references(sdk_root)
        if stale_count > 0:
            print(f"\n{YELLOW}Migration complete with {stale_count} stale reference(s) remaining.{NC}")
            print("Review and fix these manually.")
            return 1

    print(f"\n{GREEN}Migration complete!{NC}")
    if not args.dry_run:
        print("\nNext steps:")
        print("  1. Run: uv sync")
        print("  2. Run: python scripts/verify_namespace_migration.py")
        print("  3. Run: make test")
    return 0


if __name__ == "__main__":
    sys.exit(main())
