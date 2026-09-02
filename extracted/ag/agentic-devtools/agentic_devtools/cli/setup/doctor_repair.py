"""Doctor repair for corrupted install artifacts (DESTRUCTIVE, gated).

Provides:
- ``UserDeclinedRepairError``: raised when the user declines destructive repair.
- ``ArtifactCleanupResult``: per-artifact cleanup outcome.
- ``structured_cleanup()``: structured deletion mirroring ``cleanup_artifacts()`` semantics.
- ``confirm_destructive_repair()``: TTY-gated interactive confirmation.
- ``repair_corrupted_artifacts()``: main RepairFn for ``STALE_PARTIAL_INSTALL``.
"""

from __future__ import annotations

import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dependency_checker import DependencyStatus


class UserDeclinedRepairError(Exception):
    """Raised when the user declines a destructive repair operation."""


@dataclass
class ArtifactCleanupResult:
    """Outcome of a single artifact cleanup attempt."""

    path: str
    success: bool
    error: str | None = None


def structured_cleanup(artifacts: list[Path]) -> list[ArtifactCleanupResult]:
    """Remove artifacts and return structured per-artifact outcomes.

    Uses the same deletion primitives as ``cleanup_artifacts()``
    (``shutil.rmtree`` for directories, ``Path.unlink()`` for files/symlinks).
    ``FileNotFoundError`` is treated as already-cleaned (success) for TOCTOU
    safety.
    """
    results: list[ArtifactCleanupResult] = []
    for artifact in artifacts:
        try:
            if artifact.is_symlink():
                artifact.unlink()
            elif artifact.is_dir():
                shutil.rmtree(artifact)
            else:
                artifact.unlink()
            results.append(ArtifactCleanupResult(path=str(artifact), success=True))
        except FileNotFoundError:
            # TOCTOU: already removed between detection and cleanup.
            results.append(ArtifactCleanupResult(path=str(artifact), success=True))
        except (PermissionError, OSError) as exc:
            results.append(ArtifactCleanupResult(path=str(artifact), success=False, error=str(exc)))
    return results


def confirm_destructive_repair(artifacts: list[Path]) -> None:
    """Prompt the user to confirm a destructive repair.

    Prints a grouped preview of artifacts to ``sys.stderr`` and requests
    confirmation.  Raises :class:`UserDeclinedRepairError` if the user
    declines or if the environment is non-interactive (no TTY).

    Args:
        artifacts: Artifact paths to be deleted.

    Raises:
        UserDeclinedRepairError: On decline or non-interactive environment.
    """
    # Group artifacts by parent directory for display.
    grouped: dict[str, list[str]] = {}
    for artifact in artifacts:
        parent = str(artifact.parent)
        grouped.setdefault(parent, []).append(artifact.name)

    # Print preview to stderr regardless of TTY status (dry-run preview).
    print("\n⚠️  DESTRUCTIVE REPAIR — the following will be deleted:", file=sys.stderr)
    for parent_dir, names in grouped.items():
        print(f"  {parent_dir}{os.sep}", file=sys.stderr)
        for name in names:
            print(f"    {name}", file=sys.stderr)
    print(file=sys.stderr)

    # Non-interactive: treat as decline.
    if not sys.stdin.isatty():
        raise UserDeclinedRepairError("Non-interactive environment (no TTY) — cannot confirm destructive repair")

    try:
        response = input("Proceed with deletion? [y/N] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        raise UserDeclinedRepairError("User declined destructive repair") from None

    if response not in ("y", "yes"):
        raise UserDeclinedRepairError("User declined destructive repair")


def repair_corrupted_artifacts(dep: DependencyStatus) -> None:
    """Repair corrupted install artifacts (DESTRUCTIVE, gated).

    Reuses the artifact list already stored in ``dep.repair_details["detected_artifacts"]``
    by ``check_corrupted_artifacts_status()`` (NFR-003: single scan per invocation). Falls
    back to a fresh ``detect_corrupted_artifacts()`` call only when that key is absent.

    Raises ``TypeError`` if ``detected_artifacts`` is not a ``list`` of ``str``/``Path``
    entries. Raises ``ValueError`` if any resolved artifact path falls inside
    ``~/.agdt`` (user workflow state must never be deleted).

    Args:
        dep: The ``DependencyStatus`` for corrupted-install-artifacts.
    """
    raw_artifacts: list[str | Path] | None = dep.repair_details.get("detected_artifacts")
    if raw_artifacts is None:
        from .script_generators.required_setup import detect_corrupted_artifacts

        artifacts: list[Path] = detect_corrupted_artifacts()
    else:
        if not isinstance(raw_artifacts, list):
            raise TypeError(f"repair_details['detected_artifacts'] must be a list, got {type(raw_artifacts).__name__}")
        resolved: list[Path] = []
        for entry in raw_artifacts:
            if not isinstance(entry, (str, Path)):
                raise TypeError(f"Each entry in detected_artifacts must be str or Path, got {type(entry).__name__!r}")
            resolved.append(Path(entry))
        artifacts = resolved

    # Safety invariant: never delete anything under ~/.agdt (user workflow state).
    agdt_dir = Path.home() / ".agdt"
    for artifact in artifacts:
        try:
            artifact.resolve().relative_to(agdt_dir.resolve())
        except ValueError:
            pass
        else:
            raise ValueError(f"Refusing to delete artifact inside ~/.agdt (user state directory): {artifact}")

    if not artifacts:
        # No artifacts found (healthy on re-check).
        dep.found = True
        return

    # Gate behind confirmation.
    confirm_destructive_repair(artifacts)

    # Perform cleanup.
    results = structured_cleanup(artifacts)

    deleted = [r for r in results if r.success]
    failed = [r for r in results if not r.success]

    dep.repair_details["deleted_artifacts"] = [r.path for r in deleted]
    if failed:
        dep.repair_details["failed_artifacts"] = [{"path": r.path, "error": r.error} for r in failed]
        # Partial failure: dep.found stays False.
        dep.found = False
    else:
        dep.found = True
