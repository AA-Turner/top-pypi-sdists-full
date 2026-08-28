"""Is this app ready to publish? Are *all* of them?

The generated suite (:mod:`matrice_analytics.engine.testing.generate`) answers that for one app.
This module is the surface an app-repo uses: two functions, no pytest, no engine knowledge
required.

    from matrice_analytics.engine.testing import validate_app, validate_apps

    validate_app("./v1.4").ok
    result = validate_apps("applications/")
    print(result.report())
    raise SystemExit(0 if result.ok else 1)

Deliberately *not* exported from ``matrice_analytics`` itself. The engine imports no legacy module
(**PY-20**, guarded by ``tests/unit/engine/test_import_isolation.py``) and hoisting this to the
package root would pull the engine into every ``import matrice_analytics``.

A skip is not a failure. An app whose incidents cannot be driven by manifest-derived synthetic
input reports ``skipped`` with the reason written out, and still counts as ready — the gap is
recorded rather than hidden, which is the same rule the suite itself follows.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from matrice_analytics.engine.manifest.loader import MANIFEST_FILENAME
from matrice_analytics.engine.testing.generate import (
    DEFAULT_HASH_SEEDS,
    SuiteResult,
    generate_suite,
)

__all__ = ["AppsResult", "discover_apps", "validate_app", "validate_apps"]


@dataclass(frozen=True)
class AppsResult:
    """Every app under one root, and whether the whole set is ready."""

    root: Path
    results: tuple[SuiteResult, ...]

    @property
    def ok(self) -> bool:
        """``True`` when no app failed a check. An empty root is **not** ready."""
        return bool(self.results) and all(result.passed for result in self.results)

    @property
    def failures(self) -> tuple[SuiteResult, ...]:
        return tuple(result for result in self.results if not result.passed)

    def report(self) -> str:
        """One block per app, then a one-line verdict — what a CI log should show."""
        if not self.results:
            return f"no app folders found under {self.root} (an app folder holds an {MANIFEST_FILENAME})"

        lines = [result.report() for result in self.results]
        failed = self.failures
        lines.append("")
        if failed:
            names = ", ".join(result.app_id for result in failed)
            lines.append(f"{len(failed)} of {len(self.results)} app(s) NOT ready: {names}")
        else:
            lines.append(f"all {len(self.results)} app(s) ready")
        return "\n".join(lines)

    def summary(self) -> str:
        """One line per app, for when the full report is too much."""
        return "\n".join(
            f"{'PASS' if result.passed else 'FAIL'}  {result.app_id}  ({result.source})" for result in self.results
        )


def validate_app(
    app: str | os.PathLike[str],
    *,
    seeds: tuple[str, str] = DEFAULT_HASH_SEEDS,
) -> SuiteResult:
    """Run every generated check for one app folder.

    Args:
        app: An app folder, a path to its ``app.yaml``, or a bare app id.
        seeds: The two ``PYTHONHASHSEED`` values the determinism check runs under.

    Returns:
        A :class:`~matrice_analytics.engine.testing.generate.SuiteResult`; ``.passed`` is the
        verdict and ``.report()`` explains it. A manifest that does not load is a red check, not
        an exception.
    """
    return generate_suite(app, seeds=seeds)


def discover_apps(root: str | os.PathLike[str]) -> tuple[Path, ...]:
    """Every app folder under ``root``, sorted.

    An app folder is one that directly contains an ``app.yaml``. ``root`` itself counts, so a
    single app folder can be passed to :func:`validate_apps` as well as a tree of them. Nested
    apps are found, but an app folder is never descended into — a ``samples/`` directory that
    happens to hold an ``app.yaml`` fixture is not a second app.
    """
    base = Path(root)
    if (base / MANIFEST_FILENAME).is_file():
        return (base,)

    found: list[Path] = []
    for manifest in sorted(base.rglob(MANIFEST_FILENAME)):
        folder = manifest.parent
        if any(folder.is_relative_to(seen) for seen in found):
            continue
        found.append(folder)
    return tuple(found)


def validate_apps(
    root: str | os.PathLike[str],
    *,
    seeds: tuple[str, str] = DEFAULT_HASH_SEEDS,
) -> AppsResult:
    """Run every generated check for every app under ``root``.

    The "is the whole catalogue production-ready" call: one invocation, one verdict, and a report
    that names the app and the check for anything that is not.
    """
    base = Path(root)
    results = tuple(validate_app(folder, seeds=seeds) for folder in discover_apps(base))
    return AppsResult(root=base, results=results)
