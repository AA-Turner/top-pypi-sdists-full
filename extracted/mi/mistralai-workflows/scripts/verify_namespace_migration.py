#!/usr/bin/env python3
"""One-off validation script for the PEP 420 namespace migration.

Verifies that the rename from mistralai_workflows -> mistralai.workflows
is complete and correct. Run from workflow_sdk/:

    uv run python scripts/verify_namespace_migration.py
"""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path

GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"

failures = 0


def run_tests(test_dir: str, description: str) -> bool:
    """Run pytest on a test directory."""
    cmd = [
        "uv", "run",
        "pytest", test_dir,
        "-m", "not integration",
        "-v", "--tb=short",
    ]
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode == 0


def pass_msg(msg: str) -> None:
    print(f"  {GREEN}✓{NC} {msg}")


def fail_msg(msg: str) -> None:
    global failures
    failures += 1
    print(f"  {RED}✗{NC} {msg}")


# ---------------------------------------------------------------------------
# 1. SDK v2 client imports — verify mistralai.client re-exports
# ---------------------------------------------------------------------------
print("\n[1] SDK v2 client imports (mistralai.client)")

try:
    import mistralai.client as _mc

    pass_msg("import mistralai.client as mistralai")
except Exception as exc:
    fail_msg(f"import mistralai.client as mistralai: {exc}")
    _mc = None  # type: ignore[assignment]

if _mc is not None:
    for _attr in [
        "Mistral",
        "AgentCreationRequest",
        "ChatCompletionRequestMessage",
        "Output",
        "AgentCreationRequestToolTypedDict",
    ]:
        if hasattr(_mc, _attr):
            pass_msg(f"mistralai.{_attr} accessible")
        else:
            fail_msg(f"mistralai.{_attr} not found in mistralai.client")

try:
    import mistralai.extra.run.tools  # noqa: F401

    pass_msg("mistralai.extra.run.tools importable")
except Exception as exc:
    fail_msg(f"mistralai.extra.run.tools: {exc}")


# ---------------------------------------------------------------------------
# 2. Directory structure — no __init__.py at PEP 420 namespace levels
# ---------------------------------------------------------------------------
print("\n[2] Directory structure (PEP 420 namespace levels)")

sdk_root = Path(__file__).resolve().parent.parent
namespace_levels = [
    sdk_root / "mistralai" / "__init__.py",
    sdk_root / "mistralai" / "workflows" / "plugins" / "__init__.py",
    sdk_root / "plugins" / "mistralai" / "mistralai" / "__init__.py",
    sdk_root / "plugins" / "mistralai" / "mistralai" / "workflows" / "plugins" / "__init__.py",
]

for path in namespace_levels:
    rel = path.relative_to(sdk_root)
    if path.exists():
        fail_msg(f"{rel} exists (should not for PEP 420 namespace)")
    else:
        pass_msg(f"{rel} absent")

# Verify the installed mistralai package is a PEP 420 namespace (no __file__)
import mistralai

if getattr(mistralai, "__file__", None) is not None:
    fail_msg(
        f"mistralai has __file__={mistralai.__file__} — "
        "not a PEP 420 namespace package (is the TestPyPI version installed?)"
    )
else:
    pass_msg(f"mistralai is a namespace package (paths: {list(mistralai.__path__)})")


# ---------------------------------------------------------------------------
# 3. No stale references — scan .py files for leftover mistralai_workflows
# ---------------------------------------------------------------------------
print("\n[3] No stale references to mistralai_workflows")

stale_files: list[tuple[Path, int, str]] = []
scan_dirs = [sdk_root / "mistralai", sdk_root / "plugins", sdk_root / "tests"]

for scan_dir in scan_dirs:
    if not scan_dir.exists():
        continue
    for root, _dirs, files in os.walk(scan_dir):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fpath = Path(root) / fname
            try:
                lines = fpath.read_text().splitlines()
            except Exception:
                continue
            for lineno, line in enumerate(lines, 1):
                if "mistralai_workflows" in line:
                    stale_files.append((fpath, lineno, line.strip()))

# Also scan this script's sibling scripts and pyproject.toml
for extra in [sdk_root / "pyproject.toml", sdk_root / "tasks.py"]:
    if extra.exists():
        try:
            lines = extra.read_text().splitlines()
            for lineno, line in enumerate(lines, 1):
                if "mistralai_workflows" in line:
                    stale_files.append((extra, lineno, line.strip()))
        except Exception:
            pass

if stale_files:
    fail_msg(f"Found {len(stale_files)} stale reference(s):")
    for fpath, lineno, line in stale_files[:20]:
        print(f"      {fpath.relative_to(sdk_root)}:{lineno}: {line}")
    if len(stale_files) > 20:
        print(f"      ... and {len(stale_files) - 20} more")
else:
    pass_msg("No stale mistralai_workflows references found")


# ---------------------------------------------------------------------------
# 4. Core imports — import all public exports from mistralai.workflows
# ---------------------------------------------------------------------------
print("\n[4] Core imports from mistralai.workflows")

try:
    import mistralai.workflows as mw

    pass_msg("import mistralai.workflows")
except Exception as exc:
    fail_msg(f"import mistralai.workflows: {exc}")
    mw = None  # type: ignore[assignment]

if mw is not None:
    all_exports = getattr(mw, "__all__", [])
    if not all_exports:
        fail_msg("mistralai.workflows.__all__ is empty or missing")
    else:
        pass_msg(f"__all__ has {len(all_exports)} exports")
        missing = [name for name in all_exports if not hasattr(mw, name)]
        if missing:
            fail_msg(f"Missing exports: {missing}")
        else:
            pass_msg("All __all__ exports are accessible")


# ---------------------------------------------------------------------------
# 5. Plugin imports — import from mistralai.workflows.plugins.mistralai
# ---------------------------------------------------------------------------
print("\n[5] Plugin imports from mistralai.workflows.plugins.mistralai")

try:
    import mistralai.workflows.plugins.mistralai as plugin_mod

    pass_msg("import mistralai.workflows.plugins.mistralai")
    plugin_all = getattr(plugin_mod, "__all__", [])
    if plugin_all:
        pass_msg(f"Plugin __all__ has {len(plugin_all)} exports")
    else:
        fail_msg("Plugin __all__ is empty or missing")
except ImportError as exc:
    fail_msg(f"import mistralai.workflows.plugins.mistralai: {exc}")
except Exception as exc:
    fail_msg(f"import mistralai.workflows.plugins.mistralai: {exc}")


# ---------------------------------------------------------------------------
# 6. Plugin discovery — list_plugins() finds the mistralai plugin
# ---------------------------------------------------------------------------
print("\n[6] Plugin discovery via list_plugins()")

try:
    from mistralai.workflows.plugins._discovery import list_plugins

    plugins = list_plugins()
    names = [p.name for p in plugins]
    if "mistralai" in names:
        pass_msg(f"list_plugins() found {len(plugins)} plugin(s): {names}")
    else:
        fail_msg(f"list_plugins() did not find 'mistralai' plugin (found: {names})")
except Exception as exc:
    fail_msg(f"list_plugins() failed: {exc}")


# ---------------------------------------------------------------------------
# 7. Submodule imports — key submodules are importable
# ---------------------------------------------------------------------------
print("\n[7] Submodule imports")

submodules = [
    "mistralai.workflows.core.activity",
    "mistralai.workflows.core.workflow",
    "mistralai.workflows.core.worker",
    "mistralai.workflows.client",
    "mistralai.workflows.models",
]

for mod_name in submodules:
    try:
        importlib.import_module(mod_name)
        pass_msg(f"import {mod_name}")
    except Exception as exc:
        fail_msg(f"import {mod_name}: {exc}")


# ---------------------------------------------------------------------------
# 8. Core SDK unit tests — validate migration with tests
# ---------------------------------------------------------------------------
print("\n[8] Core SDK unit tests")

sdk_test_dir = str(sdk_root / "tests")
if run_tests(sdk_test_dir, "Core SDK tests"):
    pass_msg("All core SDK tests passed")
else:
    fail_msg("Core SDK tests failed")


# ---------------------------------------------------------------------------
# 9. Mistralai plugin unit tests
# ---------------------------------------------------------------------------
print("\n[9] Mistralai plugin unit tests")

plugin_test_dir = sdk_root / "plugins" / "mistralai" / "tests"
if plugin_test_dir.exists():
    if run_tests(str(plugin_test_dir), "Plugin tests"):
        pass_msg("All plugin tests passed")
    else:
        fail_msg("Plugin tests failed")
else:
    pass_msg("Plugin tests directory not found (skipped)")


# ---------------------------------------------------------------------------
# 10. Wheel structure verification (build + verify_namespace.py)
# ---------------------------------------------------------------------------
print("\n[10] Wheel structure verification")

# Build the wheel
print("  Building wheel...")
build_result = subprocess.run(["uv", "build"], cwd=sdk_root, capture_output=True, text=True)

if build_result.returncode != 0:
    fail_msg(f"Wheel build failed:\n{build_result.stderr.strip()}")
else:
    pass_msg("Wheel built successfully")

    # Run verify_namespace.py
    verify_script = sdk_root / "verify_namespace.py"
    verify_result = subprocess.run(
        [sys.executable, str(verify_script)],
        cwd=sdk_root,
        capture_output=True,
        text=True,
    )
    if verify_result.returncode == 0:
        pass_msg("Wheel PEP 420 structure verified")
    else:
        fail_msg(f"Wheel verification failed:\n{verify_result.stdout}")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
if failures:
    print(f"{RED}FAILED{NC}: {failures} check(s) failed")
    sys.exit(1)
else:
    print(f"{GREEN}PASSED{NC}: All namespace migration checks passed")
    sys.exit(0)
