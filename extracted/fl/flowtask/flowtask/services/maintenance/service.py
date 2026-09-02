"""``MaintenanceService`` — the SOC2 CC8 maintenance/status surface.

This service plugs into a Flowtask aiohttp application (server mode) and wires
three change-management surfaces:

* **Status page** — server liveness, startup-job outcome and the availability
  of the ``/api/v2/task`` and ``/api/v2/scheduler`` APIs, with every failure
  persisted (Redis, with an in-memory fallback) for auditing.
* **Changelog page** — an end-user "What's New" page built from a local
  ``CHANGELOG.md`` or the GitHub Releases API and served as HTML.
* **Maintenance windows** — an HTTP endpoint to register a window (day + hour
  range); on startup an email summary of the upcoming windows is sent via
  ``async-notify`` and the windows are advertised on the status page.

Usage (inside a Navigator ``AppHandler.configure``)::

    from flowtask.services.maintenance import MaintenanceService

    maintenance = MaintenanceService()
    maintenance.setup(self.app)
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Sequence

from aiohttp import web

from .changelog import ChangelogBuilder
from .handlers import MaintenanceHandlers
from .health import DEFAULT_REQUIRED_ENDPOINTS, build_status_report
from .models import ChangelogEntry, StatusReport
from .store import MaintenanceStore
from .windows import MaintenanceNotifier, MaintenanceWindowManager

logger = logging.getLogger(__name__)

# App key under which the running service is published for handlers/other code.
MAINTENANCE_APP_KEY = "flowtask_maintenance"


def _conf(name: str, default: Any = None) -> Any:
    """Read a value from :mod:`flowtask.conf`, tolerating an absent config."""
    try:
        import flowtask.conf as conf  # local import: conf pulls a heavy chain
    except Exception:  # pragma: no cover - conf unavailable (isolated tests)
        return default
    return getattr(conf, name, default)


class MaintenanceService:
    """Aiohttp-pluggable maintenance/status service.

    All constructor arguments are optional and fall back to
    :mod:`flowtask.conf`. This keeps the class usable both from the real
    application and from isolated unit tests (where explicit values are passed).

    Args:
        enabled: Master switch; when ``False`` :meth:`setup` is a no-op.
        redis_url: Redis DSN for the store (falls back to ``REDIS_URL``).
        service_name: Name shown on the status page.
        version: Running version (falls back to the package version).
        environment: Deployment environment (falls back to ``ENVIRONMENT``).
        required_endpoints: API prefixes asserted by the status page.
        status_path: Path of the HTML status page.
        changelog_path: Path of the HTML changelog page.
        api_prefix: Prefix for the JSON API and window management endpoints.
        github_repo: ``owner/name`` slug for GitHub-sourced changelogs.
        github_token: Optional GitHub token for the changelog source.
        changelog_file: Path to a local ``CHANGELOG.md``.
        notify_email: Recipient for the startup maintenance-window email.
        email_account: SMTP account dict for ``async-notify``.
        notify_on_startup: Whether to send the startup email at all.
    """

    def __init__(
        self,
        *,
        enabled: Optional[bool] = None,
        redis_url: Optional[str] = None,
        service_name: str = "Flowtask",
        version: Optional[str] = None,
        environment: Optional[str] = None,
        required_endpoints: Optional[Sequence[str]] = None,
        status_path: str = "/status",
        changelog_path: str = "/changelog",
        api_prefix: str = "/api/v2/maintenance",
        github_repo: Optional[str] = None,
        github_token: Optional[str] = None,
        changelog_file: Optional[Path] = None,
        notify_email: Optional[str] = None,
        email_account: Optional[dict] = None,
        notify_on_startup: Optional[bool] = None,
    ) -> None:
        self.logger = logger
        self.enabled = (
            _conf("MAINTENANCE_ENABLED", True) if enabled is None else enabled
        )
        self.service_name = service_name
        self.version = version or _conf("__version__") or self._package_version()
        self.environment = environment or _conf("ENVIRONMENT", "development")
        self.required_endpoints = tuple(
            required_endpoints or DEFAULT_REQUIRED_ENDPOINTS
        )
        self.status_path = status_path
        self.changelog_path = changelog_path
        self.api_prefix = api_prefix.rstrip("/")

        self.store = MaintenanceStore(redis_url or _conf("REDIS_URL"))
        self.windows = MaintenanceWindowManager(self.store)

        self._changelog = ChangelogBuilder(
            source_path=changelog_file or self._default_changelog_file(),
            github_repo=github_repo or _conf("MAINTENANCE_GITHUB_REPO"),
            github_token=github_token or _conf("MAINTENANCE_GITHUB_TOKEN"),
            title=_conf("MAINTENANCE_CHANGELOG_TITLE", "What's New") or "What's New",
        )
        self._changelog_entries: Optional[list[ChangelogEntry]] = None
        self._changelog_html: Optional[str] = None

        self.notify_on_startup = (
            _conf("MAINTENANCE_NOTIFY_ON_STARTUP", True)
            if notify_on_startup is None
            else notify_on_startup
        )
        self._notifier = MaintenanceNotifier(
            recipient=notify_email or self._default_notify_email(),
            account=email_account or self._default_email_account(),
        )

        self._handlers = MaintenanceHandlers(self)
        self._started_at: Optional[datetime] = None

    # -- config helpers ----------------------------------------------------
    @staticmethod
    def _package_version() -> str:
        try:
            from flowtask.version import __version__

            return __version__
        except Exception:  # pragma: no cover - version always importable
            return "unknown"

    @staticmethod
    def _default_changelog_file() -> Optional[Path]:
        base = _conf("BASE_DIR")
        if base is None:
            return None
        candidate = Path(base) / "CHANGELOG.md"
        return candidate

    @staticmethod
    def _default_notify_email() -> Optional[str]:
        explicit = _conf("MAINTENANCE_NOTIFY_EMAIL")
        if explicit:
            return explicit
        recipient = _conf("DEFAULT_RECIPIENT") or {}
        return (recipient.get("account") or {}).get("address")

    @staticmethod
    def _default_email_account() -> dict:
        return {
            "host": _conf("EMAIL_HOST"),
            "port": _conf("EMAIL_PORT", 587),
            "username": _conf("EMAIL_USERNAME"),
            "password": _conf("EMAIL_PASSWORD"),
        }

    # -- setup / signals ---------------------------------------------------
    def setup(self, app: web.Application) -> "MaintenanceService":
        """Register routes and lifecycle signals on ``app``.

        A no-op when :attr:`enabled` is ``False``.
        """
        if not self.enabled:
            self.logger.info("MaintenanceService disabled; skipping setup.")
            return self

        app[MAINTENANCE_APP_KEY] = self
        h = self._handlers
        # HTML pages
        app.router.add_get(self.status_path, h.status_html)
        app.router.add_get(self.changelog_path, h.changelog_html)
        # JSON API
        app.router.add_get(f"{self.api_prefix}/status", h.status_json)
        app.router.add_get(f"{self.api_prefix}/failures", h.failures_json)
        app.router.add_get(f"{self.api_prefix}/changelog", h.changelog_json)
        # Maintenance windows
        app.router.add_get(f"{self.api_prefix}/windows", h.windows_list)
        app.router.add_post(f"{self.api_prefix}/windows", h.windows_register)
        app.router.add_delete(
            f"{self.api_prefix}/windows/{{identifier}}", h.windows_delete
        )

        app.on_startup.append(self.on_startup)
        app.on_cleanup.append(self.on_cleanup)
        self.logger.info(
            "MaintenanceService ready: status=%s changelog=%s api=%s",
            self.status_path,
            self.changelog_path,
            self.api_prefix,
        )
        return self

    async def on_startup(self, app: web.Application) -> None:
        """Open the store, record startup, build changelog, email windows."""
        self._started_at = datetime.now(timezone.utc)
        await self.store.open()
        await self.mark_startup("maintenance_service", ok=True, detail="service started")

        # Warm the changelog cache (never fatal).
        try:
            await self._refresh_changelog()
        except Exception as err:  # pragma: no cover - best-effort warmup
            self.logger.warning("Changelog warmup failed: %s", err)

        # Email a summary of upcoming maintenance windows.
        if self.notify_on_startup:
            try:
                upcoming = await self.windows.upcoming()
                await self._notifier.notify_upcoming(upcoming)
            except Exception as err:  # pragma: no cover - notification best-effort
                self.logger.error("Maintenance startup notification failed: %s", err)

    async def on_cleanup(self, app: web.Application) -> None:
        """Close the store on shutdown."""
        await self.store.close()

    # -- public API --------------------------------------------------------
    async def mark_startup(self, name: str, *, ok: bool, detail: str = "") -> None:
        """Record the outcome of a startup job/probe (for the status page).

        Other components can call this to report whether their on-startup work
        succeeded, e.g. ``await service.mark_startup("scheduler", ok=True)``.
        """
        await self.store.set_startup(name, ok, detail)
        if not ok:
            await self.store.record_failure(f"startup:{name}", detail)

    async def build_report(self, app: web.Application) -> StatusReport:
        """Build the current :class:`StatusReport` for ``app``."""
        windows = await self.windows.all_windows()
        return await build_status_report(
            app,
            self.store,
            service=self.service_name,
            version=self.version,
            environment=self.environment,
            started_at=self._started_at,
            required_endpoints=self.required_endpoints,
            windows=windows,
        )

    async def get_changelog_entries(self) -> list[ChangelogEntry]:
        """Return cached changelog entries, loading them on first use."""
        if self._changelog_entries is None:
            await self._refresh_changelog()
        return self._changelog_entries or []

    async def get_changelog_html(self) -> str:
        """Return the cached changelog HTML, building it on first use."""
        if self._changelog_html is None:
            await self._refresh_changelog()
        return self._changelog_html or ""

    async def _refresh_changelog(self) -> None:
        """(Re)load changelog entries and re-render the HTML cache."""
        entries = await self._changelog.load_entries()
        self._changelog_entries = entries
        self._changelog_html = self._changelog.render_html(entries)
