"""Doctor framework for agdt-setup-check.

Provides:
- ``RepairRegistry``: extension point that sibling subtasks register repair
  functions into, keyed by :class:`~agentic_devtools.cli.setup.fixloop.ErrorClass`.
- ``DoctorResult``: outcome dataclass encapsulating the ``SetupReport``, detected
  problems, and per-repair outcomes from a single doctor invocation.
- ``run_doctor()``: main orchestration function that wires check → classify →
  (optional) repair → report.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from dataclasses import replace as _replace
from typing import Any

from .dependency_checker import DependencyStatus
from .exit_codes import ExitCode
from .fixloop import ErrorClass
from .report import PhaseResult, SetupReport, make_report

# ── Types ──────────────────────────────────────────────────────────────────────

RepairFn = Callable[[DependencyStatus], "bool | None"]
"""A repair callable: receives the problematic ``DependencyStatus`` and performs
the repair in-place.  May raise on failure.

Return values:
- ``True``: repair was applied (mutation occurred).
- ``False``: no-op — the dependency was already healthy (no mutation needed).
- ``None``: backward-compatible — treated as ``True`` (applied).

The function **must** update *dep* to reflect the outcome of the repair — at
minimum it must set ``dep.found = True`` (and optionally ``dep.path``,
``dep.version``) when the dependency is now available.  After the call returns,
``run_doctor()`` re-classifies *dep*; if the dependency is still flagged as a
problem (``required and not found``) the repair is recorded as a failure even
though no exception was raised."""

# A zero-argument callable that returns a RepairFn.  Factories enable lazy
# loading: the repair module is not imported until the factory is invoked at
# dispatch time.  Because lambdas cannot contain import statements, use a
# nested def when the import itself must be deferred:
#
#   def _factory() -> RepairFn:
#       from my_package import my_repair_module
#       return my_repair_module.fix_missing_dep
#
#   registry.register(ErrorClass.MISSING_DEPENDENCY, _factory)
RepairFactory = Callable[[], RepairFn]


# ── RepairRegistry ─────────────────────────────────────────────────────────────


class RepairRegistry:
    """Mapping from :class:`ErrorClass` to repair callable factories.

    Sibling subtasks (#2322, #2323, #2324) register concrete repair factories
    here without modifying ``doctor.py`` itself.

    Each registered value is a zero-argument callable (a *factory*) that returns
    the actual :data:`RepairFn`.  The factory is invoked only at dispatch time
    (inside ``run_doctor()`` when ``fix=True``), not at registration time.  This
    enables lazy imports: the heavy repair module is loaded only when a repair
    is actually needed.
    """

    def __init__(self) -> None:
        self._registry: dict[ErrorClass, RepairFactory] = {}

    def register(self, error_class: ErrorClass, factory: RepairFactory) -> None:
        """Register *factory* as the repair factory for *error_class*.

        If a factory is already registered for the same class it is silently
        replaced.

        The *factory* is a zero-argument callable that returns the actual
        :data:`RepairFn`.  It is **not** invoked at registration time — only
        when ``run_doctor()`` dispatches a repair for *error_class*.

        Args:
            error_class: The ``ErrorClass`` key this repair handles.
            factory: A zero-argument callable returning the repair function.
        """
        self._registry[error_class] = factory

    def get(self, error_class: ErrorClass) -> RepairFactory | None:
        """Return the repair factory for *error_class*, or ``None``.

        Args:
            error_class: The ``ErrorClass`` to look up.

        Returns:
            The registered callable factory, or ``None`` if none is registered.
        """
        return self._registry.get(error_class)

    def clear(self) -> None:
        """Remove all registered repair factories.

        Intended for test teardown.
        """
        self._registry.clear()


# Module-level default registry (shared across the process).
_default_registry: RepairRegistry = RepairRegistry()


def get_default_registry() -> RepairRegistry:
    """Return the process-wide default :class:`RepairRegistry`."""
    return _default_registry


# ── DoctorResult ───────────────────────────────────────────────────────────────


@dataclass
class RepairOutcome:
    """Outcome of a single attempted repair."""

    error_class: ErrorClass
    dependency: DependencyStatus
    success: bool
    error_message: str | None = None
    applied: bool = True
    """Whether the repair reported attempting a mutation.

    ``True`` when the repair function returned ``True`` or ``None`` (backward
    compat), indicating it attempted a filesystem/state change — regardless of
    whether the dependency is subsequently healthy.  ``False`` when the repair
    returned ``False`` (no-op, dependency was already OK), when the repair
    raised an exception, or when no repair factory was registered.
    """
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class DoctorResult:
    """Outcome of a single doctor invocation.

    Attributes:
        report: The structured ``SetupReport`` produced by the invocation.
        problems: Snapshot of the ``DependencyStatus`` entries that had detected
            problems at classification time (before any repair mutations).
            Entries always reflect the *pre-repair* state regardless of whether
            repairs succeeded.
        repair_outcomes: One ``RepairOutcome`` per dispatched repair.
    """

    report: SetupReport
    problems: list[DependencyStatus] = field(default_factory=list)
    repair_outcomes: list[RepairOutcome] = field(default_factory=list)


# ── Private constants ─────────────────────────────────────────────────────────

_REPAIR_NOOP_MSG = "Repair returned without error but dependency is still unavailable"

# ── Private helpers ────────────────────────────────────────────────────────────


def _classify_status(status: DependencyStatus, *, fix: bool = False) -> ErrorClass | None:
    """Return the ``ErrorClass`` for a problematic dependency, or ``None`` if OK.

    Name-based classification takes priority for well-known dependency names
    (``ca-bundle``, ``path-profile``, ``git-hooks``).  When *fix* is ``True``,
    optional managed CLIs (``gh``, ``copilot``) that are missing are classified
    as ``MANAGED_CLI_MISSING`` so that registered repair factories can install
    them.  In check-only mode (``fix=False``), missing optional CLIs are not
    considered problems.

    All other required-but-missing dependencies are classified as
    ``MISSING_DEPENDENCY``.  Optional missing deps (other than managed CLIs in
    fix mode) are not considered problems.
    """
    # ca-bundle is always classified by name match, regardless of fix mode or required flag.
    if status.name == "ca-bundle" and not status.found:
        return ErrorClass.CERT_CA_FETCH

    # Corrupted install artifacts: classified by name before the generic branch.
    if status.name == "corrupted-install-artifacts" and not status.found:
        return ErrorClass.STALE_PARTIAL_INSTALL

    if status.required and not status.found:
        if status.name == "path-profile":
            return ErrorClass.PATH_PROFILE_NOT_UPDATED
        if status.name == "git-hooks":
            return ErrorClass.GIT_HOOKS_NOT_CONFIGURED
        return ErrorClass.MISSING_DEPENDENCY

    # Managed CLI repair: only in fix mode, for optional CLIs that are missing.
    if fix and status.name in {"gh", "copilot"} and not status.found:
        return ErrorClass.MANAGED_CLI_MISSING

    return None


def _determine_exit_code(
    problems: list[DependencyStatus],
    repair_outcomes: list[RepairOutcome],
) -> int:
    """Return the final exit code given problems and repair outcomes.

    Caller invariant: ``problems`` is non-empty (healthy paths short-circuit
    before reaching this function).

    Rules:
    - All problems had successful repairs → ``OK``.
    - Any unresolved problem or failed repair → ``MISSING_REQUIRED_DEP``.
    """
    repaired_deps = {r.dependency.name for r in repair_outcomes if r.success}
    all_resolved = all(s.name in repaired_deps for s in problems)
    if all_resolved:
        return ExitCode.OK.value
    return ExitCode.MISSING_REQUIRED_DEP.value


# ── Public API ─────────────────────────────────────────────────────────────────


def run_doctor(
    statuses: list[DependencyStatus],
    *,
    fix: bool = False,
    registry: RepairRegistry | None = None,
) -> DoctorResult:
    """Run the doctor: check, (optionally) repair, and build a report.

    Args:
        statuses: Pre-collected dependency statuses (from
            ``check_all_dependencies()``).
        fix: When ``True``, dispatch repair functions from *registry* for each
            detected problem.  When ``False``, only check and report.
        registry: The :class:`RepairRegistry` to look up repairs in.  Defaults
            to the process-wide :func:`get_default_registry`.

    Returns:
        A :class:`DoctorResult` with the ``SetupReport``, detected problems,
        and (when *fix* is ``True``) per-repair outcomes.
    """
    if registry is None:
        registry = get_default_registry()

    mode = "check-fix" if fix else "check"
    classified_problems: list[tuple[ErrorClass, DependencyStatus]] = []
    repair_outcomes: list[RepairOutcome] = []
    phases: list[PhaseResult] = []
    extra_details: dict[str, Any] = {}

    # ── Phase 1: check ────────────────────────────────────────────────────────
    check_start = time.monotonic()
    for status in statuses:
        error_class = _classify_status(status, fix=fix)
        if error_class is not None:
            classified_problems.append((error_class, status))
    check_ms = int((time.monotonic() - check_start) * 1000)

    check_status = "failed" if classified_problems else "success"
    phases.append(PhaseResult(name="check", status=check_status, duration_ms=check_ms))

    # ── Short-circuit when healthy ────────────────────────────────────────────
    if not classified_problems:
        report = make_report(
            ExitCode.OK.value,
            phases=phases,
            details=extra_details,
            mode=mode,
        )
        return DoctorResult(report=report, problems=[], repair_outcomes=[])

    # Snapshot the detected state before any repair mutates deps in-place so
    # that DoctorResult.problems always reflects the *pre-repair* status.
    problems: list[DependencyStatus] = [_replace(dep, repair_details={}) for _, dep in classified_problems]

    # ── Phase 2: repair dispatch (only when --fix) ────────────────────────────
    if fix:
        # Sort by ErrorClass enum definition order; stable sort preserves
        # check-phase discovery order for same-class entries (FR-004).
        enum_order = {ec: i for i, ec in enumerate(ErrorClass)}
        classified_problems.sort(key=lambda pair: enum_order[pair[0]])

        for error_class, dep in classified_problems:
            factory = registry.get(error_class)
            if factory is None:
                phases.append(
                    PhaseResult(
                        name=f"repair:{dep.name}",
                        status="skipped",
                        error=f"No repair factory registered for {error_class.value}",
                    )
                )
                repair_outcomes.append(
                    RepairOutcome(
                        error_class=error_class,
                        dependency=dep,
                        success=False,
                        error_message=f"No repair factory registered for {error_class.value}",
                        applied=False,
                    )
                )
                continue

            repair_start = time.monotonic()
            try:
                repair_fn = factory()
                repair_result = repair_fn(dep)
                repair_ms = int((time.monotonic() - repair_start) * 1000)
                # Validate the return value before using it — unexpected types
                # (e.g. 0, "") would be treated as "applied" by `is not False`.
                # Use identity checks because 0 == False and 1 == True in Python.
                if not (repair_result is True or repair_result is False or repair_result is None):
                    raise TypeError(f"RepairFn must return True, False, or None; got {type(repair_result).__name__!r}")
                # Determine whether a mutation was applied:
                # True/None → applied=True; False → applied=False.
                applied = repair_result is not False
                # Re-classify: the repair function must have mutated *dep* to
                # reflect the fixed state.  If the problem is still present
                # (e.g. dep.found was never set to True), record the repair as
                # failed so the exit code and outcomes are never falsely positive.
                repair_failed = _classify_status(dep, fix=fix) is not None
                if repair_failed:
                    # Build descriptive error message from failed_artifacts if available.
                    failed_artifacts_raw = dep.repair_details.get("failed_artifacts", [])
                    failed_artifacts = (
                        failed_artifacts_raw if isinstance(failed_artifacts_raw, list) else [failed_artifacts_raw]
                    )
                    if failed_artifacts:
                        summaries = [
                            f"{e.get('path', '?')}: {e.get('error', '?')}" if isinstance(e, dict) else str(e)
                            for e in failed_artifacts
                        ]
                        err_msg = f"{len(failed_artifacts)} artifact(s) could not be deleted: {', '.join(summaries)}"
                    else:
                        err_msg = _REPAIR_NOOP_MSG
                    phases.append(
                        PhaseResult(
                            name=f"repair:{dep.name}",
                            status="failed",
                            duration_ms=repair_ms,
                            error=err_msg,
                        )
                    )
                    repair_outcomes.append(
                        RepairOutcome(
                            error_class=error_class,
                            dependency=dep,
                            success=False,
                            error_message=err_msg,
                            applied=applied,
                            details=dict(dep.repair_details) if dep.repair_details else {},
                        )
                    )
                else:
                    phases.append(
                        PhaseResult(
                            name=f"repair:{dep.name}",
                            status="success",
                            duration_ms=repair_ms,
                        )
                    )
                    repair_outcomes.append(
                        RepairOutcome(
                            error_class=error_class,
                            dependency=dep,
                            success=True,
                            applied=applied,
                            details=dict(dep.repair_details) if dep.repair_details else {},
                        )
                    )
            except Exception as exc:  # noqa: BLE001
                repair_ms = int((time.monotonic() - repair_start) * 1000)
                phases.append(
                    PhaseResult(
                        name=f"repair:{dep.name}",
                        status="failed",
                        duration_ms=repair_ms,
                        error=str(exc),
                    )
                )
                repair_outcomes.append(
                    RepairOutcome(
                        error_class=error_class,
                        dependency=dep,
                        success=False,
                        error_message=str(exc),
                        applied=False,
                        details=dict(dep.repair_details) if dep.repair_details else {},
                    )
                )

    # Merge repair outcome details into extra_details.
    for outcome in repair_outcomes:
        if outcome.details:
            for key, value in outcome.details.items():
                if key in extra_details:
                    existing = extra_details[key]
                    if isinstance(existing, list) and isinstance(value, list):
                        extra_details[key] = existing + value
                    # Non-list collision: earlier value wins (no overwrite).
                else:
                    extra_details[key] = value

    exit_code = _determine_exit_code(problems, repair_outcomes)
    report = make_report(
        exit_code,
        phases=phases,
        details=extra_details,
        mode=mode,
    )
    return DoctorResult(report=report, problems=problems, repair_outcomes=repair_outcomes)
