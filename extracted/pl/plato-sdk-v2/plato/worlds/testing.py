"""E2E test runner for Plato worlds.

When ``e2e_test_dir`` is set in a world's config, the world runs its
normal ``reset()`` (initializing workspaces, services, etc.) and then
executes test functions from that directory instead of the ``step()`` loop.

Tests receive the fully initialized world instance — with real workspaces,
agent spawning, services, and everything the world normally sets up.

Quick start
-----------

1. Write ``tests/e2e/test_something.py``::

    async def test_workspace_exists(world):
        ws = world.workspace("code")
        assert ws.path.exists()

    async def test_bootstrap_tasks(world):
        from webclone.verifiers.tasks import discover_tasks
        tasks = discover_tasks(world.workspace("verifier").path)
        assert len(tasks) > 0

2. Create ``tests/e2e/configs/basic.json``::

    {
      "world": {
        "package": "plato-world-webclone",
        "config": {
          "e2e_test_dir": "/extra/e2e-tests",
          ...normal world config...
        }
      },
      "dev": {
        "world": "../../..",
        "extra_sync": { "e2e-tests": ".." },
        "sync_sdk": true
      },
      "test": {
        "pass_env": ["PLATO_API_KEY"],
        "phases": [{
          "name": "e2e",
          "command": "plato-world-runner run --world plato-world-webclone --config /tmp/config.json -v"
        }]
      }
    }

3. Run::

    plato chronos test tests/e2e/configs/basic.json
"""

from __future__ import annotations

import asyncio
import importlib.util
import inspect
import logging
import sys
import time
import traceback
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing import Any as _WorldType

    from opentelemetry.trace import Tracer

logger = logging.getLogger(__name__)


async def run_e2e_tests(world: _WorldType, tracer: Tracer) -> None:
    """Discover and run e2e test functions, called from BaseWorld._run_loop.

    Args:
        world: The fully initialized world instance (after reset()).
        tracer: OTel tracer for creating per-test spans.

    Raises:
        RuntimeError: If any tests fail or error.
    """
    test_dir = Path(world.config.e2e_test_dir)
    test_filter = getattr(world.config, "e2e_test_filter", "") or ""

    if not test_dir.exists():
        raise RuntimeError(
            f"E2E test directory not found: {test_dir}  (sync it via dev.extra_sync in the test config JSON)"
        )

    test_files = sorted(test_dir.glob("test_*.py"))
    if not test_files:
        raise RuntimeError(f"No test_*.py files in {test_dir}")

    # Let test files import from each other
    if str(test_dir) not in sys.path:
        sys.path.insert(0, str(test_dir))

    passed = failed = errors = 0
    results: list[dict[str, Any]] = []

    for test_file in test_files:
        module = _import_file(test_file)
        if module is None:
            errors += 1
            results.append({"name": test_file.stem, "status": "error", "error": "import failed"})
            world.logger.error("IMPORT ERROR: %s", test_file.name)
            continue

        # Optional per-file setup/teardown
        await _call_hook(module, "setup_module", world)

        # Collect test functions
        test_fns = sorted(
            ((name, fn) for name, fn in inspect.getmembers(module, inspect.isfunction) if name.startswith("test_")),
            key=lambda x: x[0],
        )
        if test_filter:
            test_fns = [(n, f) for n, f in test_fns if test_filter in n]

        for fn_name, fn in test_fns:
            qname = f"{test_file.stem}::{fn_name}"
            with tracer.start_as_current_span(f"test.{qname}") as span:
                t0 = time.monotonic()
                try:
                    if asyncio.iscoroutinefunction(fn):
                        await fn(world)
                    else:
                        fn(world)

                    ms = (time.monotonic() - t0) * 1000
                    passed += 1
                    results.append({"name": qname, "status": "passed", "ms": round(ms)})
                    world.logger.info("PASSED  %s  (%.0fms)", qname, ms)

                except Exception as exc:
                    ms = (time.monotonic() - t0) * 1000
                    tb = traceback.format_exc()
                    from opentelemetry.trace import StatusCode

                    span.set_status(StatusCode.ERROR, str(exc))
                    span.record_exception(exc)
                    failed += 1
                    results.append({"name": qname, "status": "failed", "ms": round(ms), "error": tb})
                    world.logger.error("FAILED  %s  (%.0fms)\n%s", qname, ms, tb)

        await _call_hook(module, "teardown_module", world)

    total = passed + failed + errors
    summary = f"{passed} passed, {failed} failed, {errors} errors / {total} total"
    world.logger.info("E2E results: %s", summary)

    if failed or errors:
        raise RuntimeError(f"E2E tests failed: {summary}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _import_file(path: Path) -> Any:
    """Import a Python file by path, returning the module or None."""
    try:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)
        return module
    except Exception:
        logger.error("Failed to import %s:\n%s", path, traceback.format_exc())
        return None


async def _call_hook(module: Any, name: str, world: _WorldType) -> None:
    """Call a module-level function (setup_module/teardown_module) if it exists."""
    fn = getattr(module, name, None)
    if fn is None:
        return
    try:
        if asyncio.iscoroutinefunction(fn):
            await fn(world)
        else:
            fn(world)
    except Exception:
        logger.warning("%s failed in %s:\n%s", name, module.__name__, traceback.format_exc())
