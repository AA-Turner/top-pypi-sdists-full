"""Host-injection isolation for matrx-ai's own test suite.

WHY THIS EXISTS
---------------
``matrx_ai.configure(...)`` writes PROCESS-GLOBAL package state: the ``_ext``
host-seam registry, the durable VFS backend, the Mandate resolver, the browser
handoff ledger, the host model catalog, the capability registry. That is
correct at runtime — a host wires the package once at startup.

It is a cross-suite landmine under pytest. The aidream host bootstrap
(``aidream.package_integration.configure_packages``) runs as an IMPORT-TIME
side effect of collecting an aidream test module (e.g.
``aidream/services/mandates/tests/test_every_mandated_agent_offer.py`` calls
``_import_declaring_modules()`` at collection). Every matrx-ai test collected
afterwards then runs against a HOST-CONFIGURED package instead of the pristine
one it is asserting about:

    uv run pytest packages/matrx-ai/tests -q
        -> 4153 passed
    uv run pytest aidream/services/mandates/tests packages/matrx-ai/tests -q
        -> 13 failed  (same code, same assertions, different import order)

Measured examples of that damage:
  * ``_ext['internal_run_tracker']`` — every ``run_agent`` call opened a REAL
    host spine row against a fake ``user_id='u1'`` and refused the run
    ("PAID RUN REFUSED ... invalid input syntax for type uuid"), so tests that
    assert on what the child context saw never got there.
  * ``vfs.workspace._DURABLE_INSTALLED`` — flipped True by the host's
    ``vfs_backend``, so ``workspace_id_for`` returns the per-USER id and the
    per-conversation contract test sees ``"alice"``, not ``"alice:session-1"``.

A red run that is not a real defect is worse than no run: it trains everyone to
ignore red. So the fix is the CLASS — the leaking globals — not the assertions.

WHAT IT DOES
------------
``capture_baseline()`` is called at ``packages/matrx-ai/conftest.py`` import,
which pytest performs at session start (initial-arg conftests load before any
test module is collected/imported), i.e. BEFORE a host bootstrap can fire. The
autouse fixture restores that baseline around every matrx-ai test, so matrx-ai
tests are independent of what else is in the run and of collection order.

The restore is symmetric (before AND after): before, so an already-polluted
process is corrected; after, so a matrx-ai test that configures a seam cannot
leak into its neighbours either.

Adding a new host-injection seam to ``matrx_ai.configure``? Add it to
``_SEAMS`` here in the same commit, or the next cross-suite run goes red for
a reason nobody can find.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# Each seam: (module path, attribute names). Attributes that are dicts are
# snapshotted/restored by CONTENT (the module holds the identity); everything
# else is rebound. A module that cannot be imported here is simply not part of
# the baseline — never a hard error in a test-support path.
_SEAMS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("matrx_ai._ext", ("_registry", "_configured")),
    ("matrx_ai.db._registry", ("_models", "_bases", "_instances", "_extras", "_configured")),
    ("matrx_ai.mandates", ("_MANDATE_RESOLVER",)),
    ("matrx_ai.browser_handoff.seam", ("_LEDGER",)),
    ("matrx_ai.capabilities.registry", ("_REGISTRY",)),
    ("matrx_ai.catalog.host_catalog", ("_runtime_models",)),
    ("matrx_ai.persistence.registry", ("_policy_registrar",)),
    ("matrx_ai.tools.vfs.workspace", ("_BACKEND", "_DURABLE_INSTALLED", "_FS_CACHE")),
)


class HostSeamDriftError(RuntimeError):
    """A declared seam no longer exists — the isolation would silently not run."""


@dataclass(frozen=True)
class HostSeamBaseline:
    """Pristine values of every matrx-ai host-injection global."""

    values: dict[tuple[str, str], Any]


def capture_baseline() -> HostSeamBaseline:
    """Snapshot the package's host-injection globals as they are right now.

    Loud on drift: a seam module that will not import, or a declared attribute
    that no longer exists, raises. A silently-skipped seam is the exact failure
    mode this file exists to prevent — the isolation would still look installed
    while that global leaked freely.
    """
    import importlib

    captured: dict[tuple[str, str], Any] = {}
    drift: list[str] = []
    for module_path, attrs in _SEAMS:
        try:
            module = importlib.import_module(module_path)
        except Exception as exc:
            drift.append(f"{module_path}: not importable ({type(exc).__name__}: {exc})")
            continue
        for attr in attrs:
            if not hasattr(module, attr):
                drift.append(f"{module_path}.{attr}: no such attribute")
                continue
            value = getattr(module, attr)
            captured[(module_path, attr)] = dict(value) if isinstance(value, dict) else value
    if drift:
        raise HostSeamDriftError(
            "matrx-ai host-seam isolation is out of date — these declared seams "
            "could not be captured, so nothing would restore them and matrx-ai "
            "tests would silently become order-dependent again:\n  "
            + "\n  ".join(drift)
            + "\n\nFix _SEAMS in matrx_ai/testing/host_isolation.py."
        )
    return HostSeamBaseline(values=captured)


def restore_baseline(baseline: HostSeamBaseline) -> None:
    """Put every captured global back to its baseline value.

    Dict seams (``_registry``, ``_FS_CACHE``, ``_REGISTRY``, ``_runtime_models``)
    are restored by CONTENT — other modules hold the dict object itself, so
    rebinding the name would leave stale readers pointed at the polluted dict.
    """
    import importlib
    import sys

    for (module_path, attr), value in baseline.values.items():
        module = sys.modules.get(module_path)
        if module is None:
            module = importlib.import_module(module_path)
        current = getattr(module, attr, None)
        if isinstance(value, dict) and isinstance(current, dict):
            if current != value:
                current.clear()
                current.update(value)
            continue
        if current is not value:
            setattr(module, attr, value)
