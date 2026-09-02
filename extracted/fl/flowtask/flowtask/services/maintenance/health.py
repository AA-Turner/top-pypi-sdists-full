"""Health probes that back the status page.

The probes cover the three signals required by the task:

* the **server is up** (trivially true if a probe runs),
* the **startup job ran OK** on startup, and
* the **required APIs** (``/api/v2/task`` and ``/api/v2/scheduler``) are
  registered and reachable on the aiohttp router.

Every failing probe is also persisted through :class:`MaintenanceStore` so the
failures build an auditable trail.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Sequence

from aiohttp import web

from .models import HealthCheck, MaintenanceWindow, StatusReport
from .store import MaintenanceStore

# APIs whose presence is asserted by default (task + scheduler surfaces).
DEFAULT_REQUIRED_ENDPOINTS: tuple[str, ...] = (
    "/api/v2/task",
    "/api/v2/scheduler",
)


def _registered_paths(app: web.Application) -> list[str]:
    """Return the canonical paths of every route registered on ``app``."""
    paths: list[str] = []
    for resource in app.router.resources():
        canonical = getattr(resource, "canonical", None)
        if canonical:
            paths.append(canonical)
    return paths


def check_endpoint(app: web.Application, prefix: str) -> HealthCheck:
    """Assert that at least one route starts with ``prefix``.

    Args:
        app: The aiohttp application to introspect.
        prefix: Path prefix that must be served (e.g. ``/api/v2/task``).

    Returns:
        A :class:`HealthCheck` describing whether the API is registered.
    """
    matches = [p for p in _registered_paths(app) if p.startswith(prefix)]
    ok = bool(matches)
    detail = (
        f"{len(matches)} route(s) registered"
        if ok
        else "no route registered for this API"
    )
    return HealthCheck(name=f"api:{prefix}", ok=ok, detail=detail)


def check_server() -> HealthCheck:
    """Trivial liveness probe — if this runs, the process is up."""
    return HealthCheck(name="server", ok=True, detail="server process is running")


def check_startup(app: web.Application, startup_state: dict[str, dict]) -> HealthCheck:
    """Assert the startup job(s) ran successfully.

    Two independent signals are combined:

    1. Explicit startup outcomes recorded in the store (``startup_state``), as
       reported by components via :meth:`MaintenanceService.mark_startup`.
    2. The scheduler the app installs at startup (``app["_scheduler_"]``) — its
       presence/running state is always considered when a scheduler exists, so
       recording other startup jobs never masks a stalled scheduler.

    When neither signal is available the probe fails (the startup outcome is
    unknown rather than assumed healthy).

    Args:
        app: The aiohttp application.
        startup_state: Mapping of startup-job name to its recorded outcome.

    Returns:
        A :class:`HealthCheck` for the ``startup_job`` signal.
    """
    problems: list[str] = []
    considered = 0

    for name, record in startup_state.items():
        considered += 1
        if not record.get("ok"):
            problems.append(name)

    scheduler = app.get("_scheduler_")
    if scheduler is not None:
        considered += 1
        if not getattr(scheduler, "running", True):
            problems.append("scheduler")

    if considered == 0:
        return HealthCheck(
            name="startup_job",
            ok=False,
            detail="no startup job outcome recorded and scheduler not detected",
        )
    if problems:
        return HealthCheck(
            name="startup_job",
            ok=False,
            detail=f"startup signal(s) failed: {', '.join(sorted(problems))}",
        )
    return HealthCheck(
        name="startup_job",
        ok=True,
        detail=f"{considered} startup signal(s) ok",
    )


async def build_status_report(
    app: web.Application,
    store: MaintenanceStore,
    *,
    service: str = "Flowtask",
    version: str = "unknown",
    environment: str = "development",
    started_at: Optional[datetime] = None,
    required_endpoints: Sequence[str] = DEFAULT_REQUIRED_ENDPOINTS,
    windows: Optional[list[MaintenanceWindow]] = None,
) -> StatusReport:
    """Run every probe, persist failures, and assemble a :class:`StatusReport`.

    Args:
        app: The aiohttp application being monitored.
        store: Store used to persist failures and read startup outcomes.
        service: Service/application name.
        version: Running Flowtask version.
        environment: Deployment environment.
        started_at: Server startup time, for uptime reporting.
        required_endpoints: API prefixes that must be registered.
        windows: Upcoming maintenance windows to advertise on the page.

    Returns:
        The assembled :class:`StatusReport`.
    """
    checks: list[HealthCheck] = [check_server()]

    startup_state = await store.get_startup()
    checks.append(check_startup(app, startup_state))

    for prefix in required_endpoints:
        checks.append(check_endpoint(app, prefix))

    # Persist any failing probe so the audit trail records the incident.
    for check in checks:
        if not check.ok:
            await store.record_failure(check.name, check.detail)

    now = datetime.now(timezone.utc)
    upcoming = [w for w in (windows or []) if w.is_upcoming(now)]
    upcoming.sort(key=lambda w: (w.day, w.start_time))

    return StatusReport(
        service=service,
        version=version,
        environment=environment,
        started_at=started_at,
        checks=checks,
        upcoming_windows=upcoming,
    )
