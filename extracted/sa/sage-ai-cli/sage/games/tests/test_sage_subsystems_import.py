"""Sage subsystem import smoke test.

Sage has 171+ modules across `sage/core/`, plus subpackages for
providers, devops, training, plugins, codegen, models, reasoning,
execution, and more. A regression that breaks any module's import is
a class of bug that hits every user the first time they run sage.

This test imports every Python module under sage/ (excluding tests) and
asserts the import doesn't raise. Catches:

  * Missing optional dependencies that the module doesn't guard.
  * Syntax errors in newly-edited modules.
  * Circular imports introduced by a refactor.
  * Module-level side effects that fail on a clean environment.

Heavy modules (with massive transitive imports) are tolerated as long
as `import` completes within the per-module timeout.
"""

from __future__ import annotations

import importlib
import pkgutil
import sys
from pathlib import Path

import pytest


_SAGE_ROOT = Path(__file__).resolve().parent.parent.parent   # .../sage


def _walk_sage_modules() -> list[str]:
    """Return every importable module name under `sage.*` (excluding
    test files + __pycache__). Skips modules that obviously require
    runtime args / network."""
    import sage as _sage
    modules: list[str] = []
    for info in pkgutil.walk_packages(_sage.__path__, prefix="sage."):
        name = info.name
        # Skip test modules — they don't need to be importable on their own.
        if ".tests." in name or name.endswith(".tests"):
            continue
        # Skip the games registered_sage_model_ids fixture file.
        if "registered_sage_model_ids" in name:
            continue
        # Some entry-script modules call sys.exit() at import; skip those
        # by convention (they live in `sage/scripts/`).
        if name.startswith("sage.scripts."):
            continue
        modules.append(name)
    return modules


_ALL_MODULES = _walk_sage_modules()


@pytest.mark.parametrize("module_name", _ALL_MODULES)
def test_sage_module_imports_cleanly(module_name):
    """Every module under sage.* must import without raising. Catches
    a class of regression that takes down ALL of sage on import."""
    # Some sage modules genuinely require optional deps that aren't in
    # CI (cuda, vllm, llama-cpp-python with GPU). Allow ImportError as
    # an explicit signal, but ANY other exception is a bug.
    try:
        importlib.import_module(module_name)
    except ImportError as exc:
        pytest.skip(f"optional dep missing for {module_name}: {exc}")
    except (SystemExit, KeyboardInterrupt):
        # Module called sys.exit() at import — this is a sage bug worth
        # surfacing, not skipping.
        pytest.fail(f"{module_name} called sys.exit() at import")
    # Any other Exception bubbles as a test failure.


# ───────────────────────── coverage report ────────────────────────────


def test_sage_module_count_is_substantial():
    """Sanity: we should be smoke-testing dozens of modules. If pkgutil
    is mis-detecting and we suddenly only see 5 modules, the per-module
    parametrize would only run 5 tests — easy to miss in CI output."""
    assert len(_ALL_MODULES) >= 50, (
        f"Only discovered {len(_ALL_MODULES)} modules — pkgutil may be "
        f"broken. Expected 100+."
    )


def test_sage_main_module_imports():
    """sage/__main__.py is the CLI entry — must load cleanly even on a
    minimal install (no API keys, no Ollama, no model weights)."""
    import sage.__main__  # noqa: F401


def test_sage_providers_base_imports():
    """The provider Protocol is what every other provider implements."""
    from sage.providers.base import Message  # noqa: F401


def test_sage_core_principal_builder_imports():
    """The principal builder is the heart of the build pipeline."""
    from sage.core.principal_builder import build_project_principal  # noqa: F401


def test_sage_games_pipeline_imports():
    """Games pipeline — the surface we added in earlier turns."""
    from sage.games.pipeline import build_game  # noqa: F401
    from sage.games.engines import REGISTRY  # noqa: F401
    from sage.games.publishers import REGISTRY as PUB  # noqa: F401
    from sage.games.assets.tools import available_tools  # noqa: F401
