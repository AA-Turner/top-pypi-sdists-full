import asyncio
import typing as t

from loguru import logger

from dreadnode.app.api.client import AuthenticationError
from dreadnode.app.config import Profile
from dreadnode.app.tui.auth_flow import _platform_client
from dreadnode.app.tui.bug_report import BugReportContext
from dreadnode.app.tui.screens import (
    CapabilitiesScreen,
    ConsoleScreen,
    EnvironmentScreen,
    EvaluationsScreen,
    RawSpansScreen,
    ReportBugScreen,
    RuntimeScreen,
    SandboxScreen,
    SecretsScreen,
    SessionPickerScreen,
    TracesScreen,
    WorkspaceScreen,
)
from dreadnode.app.tui.screens.services import ServicesScreen
from dreadnode.core.log import log_buffer
from dreadnode.storage.storage import Storage

SCREEN_TYPES: dict[str, type] = {
    "traces": TracesScreen,
    "runtimes": RuntimeScreen,
    "environments": EnvironmentScreen,
    "secrets": SecretsScreen,
    "sandboxes": SandboxScreen,
    "evaluations": EvaluationsScreen,
    "console": ConsoleScreen,
    "capabilities": CapabilitiesScreen,
    "report-bug": ReportBugScreen,
}

PlatformClientFactory = t.Callable[[], tuple[t.Any, Profile]]


class ScreenHost(t.Protocol):
    def is_screen_open(self, screen_type: type[object]) -> bool: ...

    def dismiss_pushed_screens(self) -> None: ...

    def push_screen(
        self,
        screen: object,
        callback: t.Callable[[t.Any], None] | None = None,
    ) -> None: ...


class SessionView(t.Protocol):
    def sessions_snapshot(self) -> dict[str, t.Any]: ...

    def active_session_id(self) -> str | None: ...


class RuntimeView(t.Protocol):
    def runtime_info(self) -> t.Any | None: ...

    def runtime_client(self) -> t.Any: ...

    def connection_manager(self) -> t.Any: ...


class RouterActions(t.Protocol):
    def on_session_picked(self, result: str | None) -> None: ...

    def refresh_sessions_then_open_picker(self) -> None: ...

    def on_workspace_screen_dismiss(self, result: t.Any) -> None: ...

    def on_capabilities_dismiss(self, result: t.Any) -> None: ...

    def collect_mcp_servers(self) -> list[dict[str, t.Any]]: ...

    def collect_workers(self) -> list[dict[str, t.Any]]: ...

    def flash_warning(self, message: str) -> None: ...

    def handle_authentication_error(self, message: str) -> None: ...

    def consume_pending_capability_reload(self) -> bool: ...

    def reload_and_open_capabilities(self) -> None: ...

    def save_default_project(self, project_key: str) -> None: ...


class ScreenRouter:
    """Owns TUI screen-opening flows and platform screen routing."""

    def __init__(
        self,
        *,
        host: ScreenHost,
        sessions: SessionView,
        runtime: RuntimeView,
        actions: RouterActions,
        platform_client: PlatformClientFactory | None = None,
    ) -> None:
        self._host = host
        self._sessions = sessions
        self._runtime = runtime
        self._actions = actions
        self._platform_client = platform_client

    def _resolve_platform_client(self) -> PlatformClientFactory:
        return self._platform_client or _platform_client

    def open_sessions(self) -> None:
        if self._host.is_screen_open(SessionPickerScreen):
            return
        # Refresh from server first so worker-created sessions appear
        self._actions.refresh_sessions_then_open_picker()

    def open_services_screen(self) -> None:
        if self._host.is_screen_open(ServicesScreen):
            return
        servers = self._actions.collect_mcp_servers()
        workers = self._actions.collect_workers()
        self._host.dismiss_pushed_screens()
        self._host.push_screen(
            ServicesScreen(
                runtime_client=self._runtime.runtime_client(),
                servers=servers,
                workers=workers,
                collect_servers=self._actions.collect_mcp_servers,
                collect_workers=self._actions.collect_workers,
            )
        )

    def open_theme_showcase(self) -> None:
        from dreadnode.app.tui.screens.theme_showcase import ThemeShowcaseScreen

        if self._host.is_screen_open(ThemeShowcaseScreen):
            return
        self._host.dismiss_pushed_screens()
        self._host.push_screen(ThemeShowcaseScreen())

    def open_console(self) -> None:
        if self._host.is_screen_open(ConsoleScreen):
            return
        self._host.dismiss_pushed_screens()
        logger.debug("Screen push | screen=ConsoleScreen")
        self._host.push_screen(ConsoleScreen(log_buffer))

    def open_report_bug(self, *, origin: str = "conversation") -> None:
        """Open the offline-first report flow with a safe runtime snapshot."""

        if self._host.is_screen_open(ReportBugScreen):
            return
        api = None
        organization_key = None
        workspace_name = None
        try:
            api, profile = self._resolve_platform_client()()
            organization_key = profile.default_organization
            workspace_name = profile.default_workspace
        except Exception:
            logger.debug("Opening bug report without an authenticated platform client")

        runtime_info = self._runtime.runtime_info()
        sessions = self._sessions.sessions_snapshot()
        session = sessions.get(self._sessions.active_session_id() or "")
        capabilities = tuple(
            (str(capability.name), capability.version)
            for capability in getattr(runtime_info, "capabilities", [])
            if getattr(capability, "enabled", True)
        )
        context = BugReportContext.collect(
            runtime_mode=str(getattr(runtime_info, "host_type", "local")),
            active_screen=origin,
            session_id=self._sessions.active_session_id(),
            agent=getattr(getattr(session, "info", None), "agent", None),
            model=getattr(session, "model", None),
            capabilities=capabilities,
            runtime_version=getattr(runtime_info, "version", None),
        )
        conversation = self._render_conversation(session)

        self._host.dismiss_pushed_screens()
        logger.debug("Screen push | screen=ReportBugScreen origin={}", origin)
        self._host.push_screen(
            ReportBugScreen(
                context=context,
                log_entries=log_buffer.snapshot(),
                conversation=conversation,
                api=api,
                organization_key=organization_key,
                workspace_name=workspace_name,
            )
        )

    @staticmethod
    def _render_conversation(session: t.Any | None) -> str:
        if session is None:
            return ""
        lines: list[str] = []
        for entry in getattr(session, "transcript", []):
            role = str(getattr(entry, "role", "unknown"))
            content = str(getattr(entry, "content", "") or "")
            metadata = getattr(entry, "metadata", {}) or {}
            if role == "assistant" and metadata.get("thinking"):
                label = "assistant thinking"
            elif role == "tool":
                label = f"tool {metadata.get('tool_name') or 'unknown'}"
            else:
                label = role
            lines.extend((f"## {label}", "", content, ""))
        return "\n".join(lines)

    async def open_platform_screen(self, screen_name: str) -> None:
        """Open a platform browser screen.

        Async because the default-project lookup for traces/runtimes
        ends up calling the synchronous platform API client; running it
        on the TUI's event loop without ``asyncio.to_thread`` froze the
        whole UI for the duration of the HTTP round-trip. Callers in
        :mod:`dreadnode.app.tui.app` schedule this through the app's
        command worker so the key handler returns immediately.
        """
        screen_type = SCREEN_TYPES.get(screen_name)
        if screen_type and self._host.is_screen_open(screen_type):
            return
        self._host.dismiss_pushed_screens()
        logger.debug("Screen push | screen={}", screen_name)
        try:
            api, profile = self._resolve_platform_client()()

            org = profile.default_organization
            workspace = profile.default_workspace
            project = profile.default_project
            if not org or not workspace:
                self._actions.flash_warning("No org/workspace. Use /login first.")
                return

            if screen_name in ("traces", "runtimes") and not project:
                project = await asyncio.to_thread(api.get_default_project_key, org, workspace)
                if project:
                    self._actions.save_default_project(project)

            if screen_name == "traces":
                if not project:
                    self._actions.flash_warning("No default project. Use /projects first.")
                    return
                self._host.push_screen(TracesScreen(api, org, workspace, project))
            elif screen_name == "runtimes":
                self._host.push_screen(
                    RuntimeScreen(
                        api,
                        org,
                        workspace,
                        project_key=project,
                        connection_manager=self._runtime.connection_manager(),
                    )
                )
            elif screen_name == "environments":
                self._host.push_screen(EnvironmentScreen(api, org, workspace))
            elif screen_name == "secrets":
                self._host.push_screen(SecretsScreen(api))
            elif screen_name == "sandboxes":
                self._host.push_screen(SandboxScreen(api, org, workspace))
            elif screen_name == "evaluations":
                self._host.push_screen(EvaluationsScreen(api, org, workspace))
        except AuthenticationError:
            self._actions.handle_authentication_error("Session expired — please sign in again")
        except Exception as exc:
            logger.exception("Failed to open {} screen", screen_name)
            self._actions.flash_warning(str(exc))

    def open_workspaces_screen(self) -> None:
        if self._host.is_screen_open(WorkspaceScreen):
            return
        self._host.dismiss_pushed_screens()
        try:
            api, profile = self._resolve_platform_client()()
            org = profile.default_organization
            workspace = profile.default_workspace
            project = profile.default_project
            if not org:
                self._actions.flash_warning("No organization. Use /login first.")
                return
            self._host.push_screen(
                WorkspaceScreen(api, org, workspace or "", project),
                callback=self._actions.on_workspace_screen_dismiss,
            )
        except AuthenticationError:
            self._actions.handle_authentication_error("Session expired — please sign in again")
        except Exception as exc:
            logger.exception("Failed to open workspaces screen")
            self._actions.flash_warning(str(exc))

    def open_projects_screen(self) -> None:
        """Open the workspace browser pre-positioned on the current workspace's
        detail view, so the user lands directly in the project list.

        Falls back to list view if no workspace is set or the saved workspace
        is no longer accessible.
        """
        if self._host.is_screen_open(WorkspaceScreen):
            return
        self._host.dismiss_pushed_screens()
        try:
            api, profile = self._resolve_platform_client()()
            org = profile.default_organization
            workspace = profile.default_workspace
            project = profile.default_project
            if not org:
                self._actions.flash_warning("No organization. Use /login first.")
                return
            self._host.push_screen(
                WorkspaceScreen(
                    api,
                    org,
                    workspace or "",
                    project,
                    start_in_detail=bool(workspace),
                ),
                callback=self._actions.on_workspace_screen_dismiss,
            )
        except AuthenticationError:
            self._actions.handle_authentication_error("Session expired — please sign in again")
        except Exception as exc:
            logger.exception("Failed to open projects screen")
            self._actions.flash_warning(str(exc))

    def open_capabilities_screen(self, initial_capability: str | None = None) -> None:
        if self._host.is_screen_open(CapabilitiesScreen):
            return
        # Always consume the pending-reload flag so it can't leak into a later
        # open. Only take the reload fast path on an untargeted open, though:
        # a targeted jump (e.g. from the services screen) skips the server
        # reload so the explicit nav target wins — its own _load_data fetch
        # is treated as fresh enough.
        if self._actions.consume_pending_capability_reload() and initial_capability is None:
            self._actions.reload_and_open_capabilities()
            return
        self._host.dismiss_pushed_screens()
        logger.debug("Screen push | screen=CapabilitiesScreen")
        try:
            api = None
            org: str | None = None
            workspace: str | None = None
            runtime_id: str | None = None

            try:
                api_client, profile = self._resolve_platform_client()()
                api = api_client
                org = profile.default_organization
                workspace = profile.default_workspace
            except AuthenticationError:
                raise
            except Exception:
                logger.debug("Not logged in to platform; opening local-only capabilities screen")

            runtime_info = self._runtime.runtime_info()
            if runtime_info is not None:
                runtime_id = getattr(runtime_info, "runtime_id", None)

            is_sandbox = getattr(runtime_info, "host_type", "local") == "sandbox"
            self._host.push_screen(
                CapabilitiesScreen(
                    runtime_client=self._runtime.runtime_client(),
                    api=api,
                    org=org,
                    workspace=workspace,
                    runtime_id=runtime_id,
                    is_sandbox=is_sandbox,
                    initial_capability=initial_capability,
                ),
                callback=self._actions.on_capabilities_dismiss,
            )
        except AuthenticationError:
            self._actions.handle_authentication_error("Session expired — please sign in again")
        except Exception as exc:
            logger.exception("Failed to open capabilities screen")
            self._actions.flash_warning(str(exc))

    def open_raw_spans_screen(self) -> None:
        if self._host.is_screen_open(RawSpansScreen):
            return
        session_id = self._sessions.active_session_id()
        if session_id is None:
            self._actions.flash_warning("No active session. Start or resume a session first.")
            return

        spans_path = Storage().session_spans_path(session_id)
        if not spans_path.exists():
            self._actions.flash_warning("No local spans file exists for this session yet.")
            return

        self._host.dismiss_pushed_screens()
        self._host.push_screen(
            RawSpansScreen(
                spans_path,
                session_id=session_id,
            )
        )
