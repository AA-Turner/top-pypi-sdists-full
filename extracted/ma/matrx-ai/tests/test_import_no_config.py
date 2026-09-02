"""Regression guard: importing matrx-ai NEVER requires ``matrx_ai.configure()``.

The package contract (CLAUDE.md / ``_ext.py`` / ``db/_registry.py``) is that a
missing host configuration raises at CALL time, never at IMPORT time. This
broke once: ``matrx_ai/tools/logger.py`` did a module-level
``from matrx_ai.db import cxm``, which eagerly built the cx_ manager singletons
from host-injected ORM bases and blew up ``import matrx_ai.tools`` with
``DBNotConfiguredError`` in any unconfigured environment.

The import must run in a SUBPROCESS: the pytest process itself (via conftest
and sibling tests) already imported matrx_ai and may have installed stub DB
configs, which would mask the regression.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

# Modules that historically resolved host-injected DB bases at module scope.
# Each must now import cleanly with zero configuration.
_IMPORT_TARGETS = [
    "matrx_ai.tools",
    "matrx_ai.db.cx_managers",
    "matrx_ai.db.agx_manager",
    "matrx_ai.db.arm_managers",
    "matrx_ai.db.conversation_rebuild",
    "matrx_ai.db.guest_registry",
    "matrx_ai.db.content_types.notes",
    "matrx_ai.db.content_types.tasks",
    "matrx_ai.tools.tool_binding_db",
    "matrx_ai.tools.tool_executor_db",
    # Client-host import surface (matrx-local): the local-LLM bridge imports
    # GenericOpenAIChat + the unified-client registry BEFORE any configure()
    # with DB wiring. unified_client historically imported ai_model_manager at
    # module scope (whose impl resolves get_model("AiModel")) — that broke
    # `from matrx_ai.providers.generic_openai import GenericOpenAIChat` in
    # every client host.
    "matrx_ai.providers",
    "matrx_ai.providers.unified_client",
    "matrx_ai.providers.generic_openai",
    # Reachable from the client-host execution path; each resolved cxm /
    # ai_model_manager at module scope before 0.3.0.
    "matrx_ai.db.conversation_gate",
    "matrx_ai.db.persistence",
    "matrx_ai.orchestrator",
    "matrx_ai.orchestrator.executor",
    "matrx_ai.catalog",
    # memory storage resolved cxm (host ORM managers) at module scope pre-0.3.1.
    "matrx_ai.memory.storage_db",
    "matrx_ai.memory.factory",
]


def _clean_env() -> dict[str, str]:
    # Minimal environment: no PYTEST_* / MATRX_* leakage, no PYTHONSTARTUP,
    # no conftest side effects (a fresh `python -c` never loads conftest.py,
    # but scrub anyway so an env-driven code path can't accidentally configure).
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", ""),
        "LANG": os.environ.get("LANG", "en_US.UTF-8"),
    }
    if "VIRTUAL_ENV" in os.environ:
        env["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV"]
    return env


@pytest.mark.parametrize("module", _IMPORT_TARGETS)
def test_import_without_configure(module: str) -> None:
    proc = subprocess.run(
        [sys.executable, "-c", f"import {module}"],
        capture_output=True,
        text=True,
        env=_clean_env(),
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        timeout=120,
    )
    assert proc.returncode == 0, (
        f"`import {module}` failed in an unconfigured environment — a module "
        f"is resolving host-injected DB bases at import time (config errors "
        f"must surface at CALL time, never import time).\n"
        f"stderr:\n{proc.stderr}"
    )


def test_db_access_still_raises_at_call_time() -> None:
    # The laziness must not silently swallow the unconfigured state: touching a
    # manager without configure() still raises DBNotConfiguredError.
    code = (
        "import matrx_ai.db.cx_managers as m\n"
        "from matrx_ai.db._registry import DBNotConfiguredError\n"
        "try:\n"
        "    m.cxm\n"
        "except DBNotConfiguredError:\n"
        "    raise SystemExit(0)\n"
        "raise SystemExit('cxm resolved without configure()')\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=_clean_env(),
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


# ---------------------------------------------------------------------------
# Structural pin: the providers ↔ orchestrator cycle class
# ---------------------------------------------------------------------------
#
# matrx-local hit a circular-import crash cold-importing matrx_ai.providers:
# providers modules pull matrx_ai.orchestrator.requests / execution_state at
# module scope, and orchestrator/__init__ used to EAGERLY import the executor
# — whose huge closure reaches back into matrx_ai.providers. One module-scope
# ``from matrx_ai.providers import X`` anywhere in that closure turns a cold
# providers import into a crash. The fix made orchestrator/__init__ a lazy
# facade; this test pins the structure by asserting the executor NEVER lands
# in the providers import closure. If this fails, the cycle class is back.


def test_providers_import_does_not_pull_executor() -> None:
    code = (
        "import sys\n"
        "import matrx_ai.providers\n"
        "heavy = [m for m in ("
        "'matrx_ai.orchestrator.executor',"
        "'matrx_ai.orchestrator.concurrent_engine',"
        "'matrx_ai.orchestrator.parallel_executor') if m in sys.modules]\n"
        "assert not heavy, f'executor closure leaked into providers import: {heavy}'\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=_clean_env(),
        timeout=120,
    )
    assert proc.returncode == 0, (
        "`import matrx_ai.providers` pulled the orchestrator executor closure "
        "back in — the providers ↔ orchestrator circular-import class is "
        f"re-armed.\nstderr:\n{proc.stderr}"
    )


@pytest.mark.parametrize(
    "order",
    [
        ("matrx_ai.providers", "matrx_ai.orchestrator"),
        ("matrx_ai.orchestrator", "matrx_ai.providers"),
        ("matrx_ai.providers", "matrx_ai.orchestrator.executor"),
        ("matrx_ai.orchestrator.executor", "matrx_ai.providers"),
        ("matrx_ai.db.persistence", "matrx_ai.providers"),
        ("matrx_ai.providers.unified_client", "matrx_ai.orchestrator.executor"),
    ],
)
def test_import_order_independence(order: tuple[str, str]) -> None:
    """Each pair must import cleanly in BOTH orders, each as the FIRST matrx_ai
    import of a fresh process — the exact condition matrx-local's
    'import matrx_ai.orchestrator first' workaround papered over."""
    first, second = order
    proc = subprocess.run(
        [sys.executable, "-c", f"import {first}; import {second}"],
        capture_output=True,
        text=True,
        env=_clean_env(),
        timeout=120,
    )
    assert proc.returncode == 0, (
        f"`import {first}` then `import {second}` failed in a fresh process — "
        f"import-order dependence regressed.\nstderr:\n{proc.stderr}"
    )


def test_orchestrator_lazy_facade_resolves_public_names() -> None:
    code = (
        "from matrx_ai.orchestrator import execute_until_complete, "
        "AIMatrixRequest, CompletedRequest\n"
        "assert callable(execute_until_complete)\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=_clean_env(),
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
