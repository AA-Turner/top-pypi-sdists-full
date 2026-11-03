"""E2E test runner for Plato worlds."""

from __future__ import annotations

import asyncio
import importlib.util
import inspect
import logging
import sys
import time
import traceback
from pathlib import Path
from types import ModuleType
from typing import Protocol

from opentelemetry.trace import StatusCode

logger = logging.getLogger(__name__)


class _SpanContext(Protocol):
    def __enter__(self) -> _SpanContext: ...

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> object: ...

    def set_status(self, *args: object) -> object: ...

    def record_exception(self, *args: object) -> object: ...


class _TracerLike(Protocol):
    def start_as_current_span(self, name: str) -> _SpanContext: ...


async def run_e2e_tests(
    world: object,
    tracer: _TracerLike,
    *,
    test_dir: str = "",
    test_filter: str = "",
) -> None:
    """Discover and run e2e test functions, called from BaseWorld._run_e2e_loop."""
    test_dir_path = Path(test_dir)

    if not test_dir_path.exists():
        raise RuntimeError(
            f"E2E test directory not found: {test_dir}  (sync it via dev.extra_sync in the test config JSON)"
        )

    test_files = sorted(test_dir_path.glob("test_*.py"))
    if not test_files:
        raise RuntimeError(f"No test_*.py files in {test_dir_path}")

    if str(test_dir_path) not in sys.path:
        sys.path.insert(0, str(test_dir_path))

    passed = 0
    failed = 0
    errors = 0
    results: list[dict[str, object]] = []

    for test_file in test_files:
        module = _import_file(test_file)
        if module is None:
            # When a filter is active, only count import failures as errors
            # if the file could contain matching tests (filter appears in filename).
            if test_filter and test_filter not in test_file.stem:
                logger.debug("Skipping import-failed file %s (no filter match)", test_file.name)
                continue
            errors += 1
            results.append({"name": test_file.stem, "status": "error", "error": "import failed"})
            _world_logger(world).error("IMPORT ERROR: %s", test_file.name)
            continue

        test_fns = sorted(
            ((name, fn) for name, fn in inspect.getmembers(module, inspect.isfunction) if name.startswith("test_")),
            key=lambda item: item[0],
        )
        if test_filter:
            test_fns = [(name, fn) for name, fn in test_fns if test_filter in name]

        if not test_fns:
            continue

        await _call_hook(module, "setup_module", world)

        for fn_name, fn in test_fns:
            qualified_name = f"{test_file.stem}::{fn_name}"
            with tracer.start_as_current_span(f"test.{qualified_name}") as span:
                started_at = time.monotonic()
                try:
                    if asyncio.iscoroutinefunction(fn):
                        await fn(world)
                    else:
                        fn(world)

                    elapsed_ms = (time.monotonic() - started_at) * 1000
                    passed += 1
                    results.append({"name": qualified_name, "status": "passed", "ms": round(elapsed_ms)})
                    _world_logger(world).info("PASSED  %s  (%.0fms)", qualified_name, elapsed_ms)
                except Exception as exc:
                    elapsed_ms = (time.monotonic() - started_at) * 1000
                    tb = traceback.format_exc()
                    span.set_status(StatusCode.ERROR, str(exc))
                    span.record_exception(exc)
                    failed += 1
                    results.append(
                        {
                            "name": qualified_name,
                            "status": "failed",
                            "ms": round(elapsed_ms),
                            "error": tb,
                        }
                    )
                    _world_logger(world).error("FAILED  %s  (%.0fms)\n%s", qualified_name, elapsed_ms, tb)

        await _call_hook(module, "teardown_module", world)

    total = passed + failed + errors
    summary = f"{passed} passed, {failed} failed, {errors} errors / {total} total"
    _world_logger(world).info("E2E results: %s", summary)

    if failed or errors:
        raise RuntimeError(f"E2E tests failed: {summary}")


def _import_file(path: Path) -> ModuleType | None:
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


async def _call_hook(module: ModuleType, name: str, world: object) -> None:
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


def _world_logger(world: object) -> logging.Logger:
    logger_obj = getattr(world, "logger", None)
    if isinstance(logger_obj, logging.Logger):
        return logger_obj
    return logger
