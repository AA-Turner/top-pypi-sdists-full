"""Slash command dispatcher for the Dreadnode TUI.

The TUI recognises ~40 slash commands (see
:data:`dreadnode.app.tui.commands.SLASH_COMMANDS`). This module owns the
dispatch table that maps each command keyword to a concrete action, plus
the simple command implementations that aren't worth spinning out into
their own managers: thinking-effort control, workspace info, platform
listings, pull-artifact, skill loading, and notification helpers.

The dispatch table used to live inline in ``DreadnodeTextualApp._handle_command``,
a 145-line method mixing routing logic with auth gating with per-command
argument handling with a skill-name fallback. Moving it here makes the
routing table into a real first-class concept and removes ~200+ lines of
scaffolding from ``app.py``.

Heavyweight command bodies that are tightly coupled to Textual widgets or
the turn lifecycle stay on ``DreadnodeTextualApp`` and are reached via the
:class:`CommandActions` port — specifically ``_update_command`` (subprocess
+ reactives + welcome-banner mutations), ``_compact_command`` (turn
lifecycle + transcript rebuild), and the ``_open_*_dialog`` methods
(Textual ``@work`` dialog openers). The dispatcher calls these by name
through the port so that the app can decide whether a command body is a
local method or something to forward to a manager.
"""

import typing as t

from loguru import logger
from textual.notifications import Notification, SeverityLevel

from dreadnode.app.client.models import RuntimeInfo
from dreadnode.app.config import Profile
from dreadnode.app.tui.commands import SLASH_COMMANDS

if t.TYPE_CHECKING:
    from dreadnode.app.client.managed_client import ManagedRuntimeClient


# =============================================================================
# Port — the single surface the dispatcher uses to talk to the app
# =============================================================================
#
# This is intentionally a fat port rather than several small ones. The
# command dispatcher touches almost every other TUI subsystem (UI status,
# runtime transport, profile/model/screen managers, turn lifecycle
# wrappers), so splitting it four ways would mostly add indirection
# without reducing the surface. The port lives next to the consumer and
# the app implements it via a narrow ``_AppCommandActions`` adapter.


class CommandActions(t.Protocol):
    """Everything :class:`CommandDispatcher` needs from the hosting app."""

    # ------------------------------------------------------------------
    # Status, flash, activity
    # ------------------------------------------------------------------

    def flash(self, message: str, *, severity: str = "info") -> None: ...

    def write_activity(self, message: str, *, style: str = "info") -> None: ...

    def set_status(self, text: str, *, busy: bool | None = None) -> None: ...

    def dismiss_welcome(self) -> None: ...

    def show_help(self) -> None: ...

    def copy_last_assistant(self) -> None: ...

    def write_session_listing(self) -> None: ...

    def write_agent_listing(self) -> None: ...

    def write_whoami(
        self,
        *,
        name: str,
        profile: Profile,
    ) -> None: ...

    def post_notification(self, notification: Notification) -> None: ...

    def unnotify(self, notification: Notification) -> None: ...

    def notification_timeout(self) -> float: ...

    # Test-friendly routing: the app exposes ``_notify_tracked`` /
    # ``_dismiss_notification`` as 1-line delegations, and tests
    # monkeypatch them to assert on routing. The dispatcher calls through
    # the port adapter methods below so those monkeypatches intercept.

    def notify_tracked(
        self,
        message: str,
        *,
        title: str = "",
        severity: SeverityLevel = "information",
        timeout: float | None = None,
        markup: bool = True,
    ) -> Notification: ...

    def dismiss_notification(self, notification: Notification | None) -> None: ...

    # ------------------------------------------------------------------
    # Reactive state
    # ------------------------------------------------------------------

    def authenticated(self) -> bool: ...

    def current_model(self) -> str: ...

    def on_model_changed(self, model_id: str) -> None: ...

    def thinking_enabled(self) -> bool: ...

    def set_thinking_enabled(self, value: bool) -> None: ...

    def effort_label(self) -> str: ...

    def set_effort_label(self, value: str) -> None: ...

    def set_show_thinking(self, value: bool) -> None: ...

    def model_variants(self) -> dict[str, str]: ...

    def set_skill_names(self, skill_names: set[tuple[str, str]]) -> None: ...

    def skill_names(self) -> set[tuple[str, str]]: ...

    def current_profile(self) -> Profile | None: ...

    def set_current_profile(self, profile: Profile) -> None: ...

    # ------------------------------------------------------------------
    # Runtime transport
    # ------------------------------------------------------------------

    def managed_client(self) -> "ManagedRuntimeClient": ...

    def local_runtime_client(self) -> "ManagedRuntimeClient": ...

    # ------------------------------------------------------------------
    # Async command runner and orchestration
    # ------------------------------------------------------------------

    def run_command(
        self,
        coro_fn: t.Callable[..., t.Awaitable[t.Any]],
        *args: t.Any,
    ) -> None:
        """Spawn ``coro_fn(*args)`` as a tracked worker with auth-error recovery."""
        ...

    async def refresh_server_sessions(self, *, include_platform: bool = False) -> None: ...

    async def apply_runtime_info(
        self,
        runtime_info: RuntimeInfo,
        *,
        refresh_skills: bool,
    ) -> None: ...

    def start_agent_session(self, agent_name: str) -> None: ...

    def send_chat(self, message: str) -> None: ...

    def create_new_session(self, agent: str | None = None) -> None: ...

    def rename_session(self, title: str) -> None: ...

    def export_session(self, filename: str | None) -> None: ...

    async def set_session_policy_command(self, args: list[str], policy_name: str) -> None: ...

    async def policy_command(self, args: list[str]) -> None: ...

    async def launch_background_task_command(self, args: list[str]) -> None: ...

    def handle_authentication_error(self, message: str) -> None: ...

    # Heavy command bodies that stay on the app.
    async def update_command_body(self) -> None: ...

    async def compact_command_body(self, args: list[str]) -> None: ...

    async def rewind_command_body(self) -> None: ...

    def open_skills_dialog(self) -> None: ...

    def open_tools_dialog(self) -> None: ...

    async def persist_default_model_choice(self, model: str) -> None: ...

    # ------------------------------------------------------------------
    # External managers used by the dispatch table
    # ------------------------------------------------------------------

    def screen_router_open_sessions(self) -> None: ...
    def screen_router_open_workspaces_screen(self) -> None: ...
    def screen_router_open_projects_screen(self) -> None: ...
    def screen_router_open_platform_screen(self, name: str) -> None: ...
    def screen_router_open_console(self) -> None: ...
    def screen_router_open_report_bug(self) -> None: ...
    def screen_router_open_raw_spans_screen(self) -> None: ...
    def screen_router_open_capabilities_screen(self) -> None: ...
    def screen_router_open_services_screen(self) -> None: ...
    def screen_router_open_theme_showcase(self) -> None: ...
    def model_manager_open_model_browser_screen(self) -> None: ...
    def profile_manager_login_command(self, args: list[str]) -> t.Awaitable[None]: ...
    def profile_manager_logout_command(self) -> t.Awaitable[None]: ...
    def profile_manager_switch_profile(self, args: list[str]) -> t.Awaitable[None]: ...
    def profile_manager_open_profile_dialog(self) -> None: ...
    def profile_manager_apply_auth_profile(self, profile: Profile) -> t.Awaitable[bool]: ...

    def exit_app(self) -> None: ...

    # ------------------------------------------------------------------
    # Profile / platform / package access
    # ------------------------------------------------------------------
    #
    # These are method hooks on the adapter rather than direct imports on
    # :class:`CommandDispatcher` so that tests which monkeypatch
    # ``dreadnode.app.tui.app._active_profile`` (or ``_platform_client``,
    # or ``Package.pull``) see their patches take effect — the adapter
    # resolves each bare name inside ``app.py``'s module namespace at
    # call time.

    def active_profile(self) -> tuple[str | None, Profile | None]: ...

    def platform_client(self) -> tuple[t.Any, Profile]: ...

    def save_profile(self, name: str, profile: Profile) -> Profile: ...

    def parse_pull_ref(self, raw: str, *, default_org: str) -> tuple[str, t.Any]: ...

    def package_pull(self, *args: t.Any, **kwargs: t.Any) -> t.Any: ...

    def make_storage(self, *, profile: Profile, api: t.Any) -> t.Any: ...


# =============================================================================
# CommandDispatcher
# =============================================================================


# Commands that work without platform authentication. All others are gated
# by the auth check at the top of :meth:`handle_command`.
_UNAUTHENTICATED_COMMANDS: frozenset[str] = frozenset(
    {
        "quit",
        "exit",
        "q",
        "help",
        "login",
        "profile",
        "profiles",
        "console",
        "report-bug",
        "thinking",
        "version",
        "update",
        "spans",
    }
)


class CommandDispatcher:
    """Routes slash commands to concrete actions.

    Owns the dispatch table, the thinking-effort state machine, and the
    simple command implementations (whoami, workspace info, workspaces,
    projects, models, pull, list sessions, reload capabilities, skill
    loading, notification helpers). Everything else is reached via
    :class:`CommandActions`.
    """

    def __init__(self, *, actions: CommandActions) -> None:
        self._actions = actions

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def handle_command(self, raw: str) -> None:
        parts = raw[1:].split()
        cmd = parts[0].lower() if parts else ""
        args = parts[1:]

        if not self._actions.authenticated() and cmd not in _UNAUTHENTICATED_COMMANDS:
            self._actions.flash(
                "Not authenticated — use /login to connect to the platform",
                severity="warning",
            )
            return

        dispatch: dict[str, t.Callable[[], None]] = {
            "quit": self._actions.exit_app,
            "exit": self._actions.exit_app,
            "q": self._actions.exit_app,
            "help": self._actions.show_help,
            "new": lambda: self._actions.create_new_session(),
            "clear": lambda: self._actions.create_new_session(),
            "reset": lambda: self._actions.create_new_session(),
            "sessions": self._actions.screen_router_open_sessions,
            "agents": self._actions.write_agent_listing,
            "reload": lambda: self._actions.run_command(self.reload_capabilities_command),
            "login": lambda: self._actions.run_command(
                self._actions.profile_manager_login_command, args
            ),
            "logout": lambda: self._actions.run_command(
                self._actions.profile_manager_logout_command
            ),
            "workspace": lambda: (
                self._actions.screen_router_open_workspaces_screen()
                if not args
                else self._actions.run_command(self.switch_workspace_command, args)
            ),
            "workspaces": self._actions.screen_router_open_workspaces_screen,
            "models": self._actions.model_manager_open_model_browser_screen,
            "runtimes": lambda: self._actions.screen_router_open_platform_screen("runtimes"),
            "environments": lambda: self._actions.screen_router_open_platform_screen(
                "environments"
            ),
            "env": lambda: self._actions.screen_router_open_platform_screen("environments"),
            "secrets": lambda: self._actions.screen_router_open_platform_screen("secrets"),
            "console": self._actions.screen_router_open_console,
            "report-bug": self._actions.screen_router_open_report_bug,
            "traces": lambda: self._actions.screen_router_open_platform_screen("traces"),
            "spans": self._actions.screen_router_open_raw_spans_screen,
            "sandboxes": lambda: self._actions.screen_router_open_platform_screen("sandboxes"),
            "evaluations": lambda: self._actions.screen_router_open_platform_screen("evaluations"),
            "capabilities": self._actions.screen_router_open_capabilities_screen,
            "caps": self._actions.screen_router_open_capabilities_screen,
            "mcp": self._actions.screen_router_open_services_screen,
            "workers": self._actions.screen_router_open_services_screen,
            "copy": self._actions.copy_last_assistant,
            "compact": lambda: self._actions.run_command(self._actions.compact_command_body, args),
            "rewind": lambda: self._actions.run_command(self._actions.rewind_command_body),
            "tools": self._actions.open_tools_dialog,
            "update": lambda: self._actions.run_command(self._actions.update_command_body),
            "theme": self._actions.screen_router_open_theme_showcase,
            "auto": lambda: self._actions.run_command(
                self._actions.set_session_policy_command, args, "headless"
            ),
            "interactive": lambda: self._actions.run_command(
                self._actions.set_session_policy_command, args, "interactive"
            ),
            "policy": lambda: self._actions.run_command(self._actions.policy_command, args),
            "background": lambda: self._actions.run_command(
                self._actions.launch_background_task_command, args
            ),
            "bg": lambda: self._actions.run_command(
                self._actions.launch_background_task_command, args
            ),
        }

        if cmd in dispatch:
            dispatch[cmd]()
            return

        # Commands with required arguments, specific argument handling, or
        # skill-name fallbacks — kept as explicit branches for clarity.
        if cmd == "agent":
            if not args:
                self._actions.flash("Usage: /agent <name>", severity="warning")
            else:
                self._actions.start_agent_session(args[0])
            return

        if cmd == "model":
            if not args:
                self._actions.flash(
                    f"Current model: {self._actions.current_model()}",
                    severity="info",
                )
            else:
                # Per-session change only. We deliberately do NOT persist the
                # profile default here (CAP-1048) — that would cause /model in
                # one session to silently change the model for every other
                # session that reads from the profile on next refresh.
                self._actions.on_model_changed(args[0])
                self._actions.flash(f"Model set to {args[0]}", severity="info")
            return

        if cmd == "pull":
            if not args:
                self._actions.flash(
                    "Usage: /pull <type://[org/]name[@version]>", severity="warning"
                )
            else:
                self._actions.run_command(self.pull_command, args[0])
            return

        if cmd == "version":
            from dreadnode.version import VERSION

            self._actions.flash(f"Dreadnode v{VERSION}", severity="info")
            return

        if cmd in {"whoami", "getuid"}:
            self._actions.run_command(self.whoami_command)
            return

        if cmd in {"profile", "profiles"}:
            if args:
                self._actions.run_command(self._actions.profile_manager_switch_profile, args)
            else:
                self._actions.profile_manager_open_profile_dialog()
            return

        if cmd == "projects":
            if args:
                self._actions.run_command(self.projects_command, args)
            else:
                self._actions.screen_router_open_projects_screen()
            return

        if cmd == "rename":
            if not args:
                self._actions.flash("Usage: /rename <title>", severity="warning")
            else:
                new_title = " ".join(args)
                self._actions.rename_session(new_title)
            return

        if cmd == "export":
            filename = args[0] if args else None
            self._actions.export_session(filename)
            return

        if cmd == "thinking":
            self.handle_thinking_command(args)
            return

        if cmd == "skills":
            self._actions.open_skills_dialog()
            return

        # Skills dispatch (CAP-IDENT-017): accept a qualified identifier exactly,
        # or a bare name that appears as the suffix of any known qualified id
        # (the server-side resolver handles unambiguous vs. ambiguous). Bundled
        # skills have no capability prefix, so their qualified id *is* bare and
        # also matches here.
        known_qualified = {name for name, _desc in self._actions.skill_names()}
        known_bares = {q.rsplit(":", 1)[-1] for q in known_qualified}
        if cmd in known_qualified or cmd in known_bares:
            self._actions.run_command(self.load_skill_command, cmd, " ".join(args))
            return

        self._actions.flash(f"Unknown command: /{cmd}", severity="warning")

    # ------------------------------------------------------------------
    # Thinking / effort control
    # ------------------------------------------------------------------

    def handle_thinking_command(self, args: list[str]) -> None:
        """Handle ``/thinking`` for effort level control."""
        from dreadnode.app.tui.model_variants import get_variants

        if not args:
            if self._actions.thinking_enabled() and self._actions.effort_label():
                self._actions.flash(
                    f"Thinking: enabled ({self._actions.effort_label()})",
                    severity="info",
                )
            else:
                self._actions.flash("Thinking: disabled", severity="info")
            return

        arg = args[0].lower()

        if arg == "show":
            self._actions.set_show_thinking(True)
            self._actions.flash("Thinking blocks visible", severity="info")
            return

        if arg == "hide":
            self._actions.set_show_thinking(False)
            self._actions.flash("Thinking blocks hidden", severity="info")
            return

        if arg == "off":
            self._actions.set_thinking_enabled(False)
            self._actions.model_variants()[self._actions.current_model()] = ""
            self._actions.set_effort_label("")
            self._actions.flash("Thinking disabled", severity="info")
            return

        variants = get_variants(self._actions.current_model())

        if arg == "on":
            if not variants:
                self._actions.flash(
                    f"Model {self._actions.current_model()} does not support thinking",
                    severity="warning",
                )
                return
            self._actions.set_thinking_enabled(True)
            label = next(iter(variants))
            self._actions.model_variants()[self._actions.current_model()] = label
            self._actions.set_effort_label(label)
            self._actions.flash(f"Thinking enabled ({label})", severity="info")
            return

        # Named effort level
        if arg in variants:
            self._actions.set_thinking_enabled(True)
            self._actions.model_variants()[self._actions.current_model()] = arg
            self._actions.set_effort_label(arg)
            self._actions.flash(f"Thinking: {arg}", severity="info")
            return

        available = ", ".join(variants.keys()) if variants else "none for this model"
        self._actions.flash(
            f"Unknown effort level '{arg}'. Available: {available}",
            severity="warning",
        )

    # ------------------------------------------------------------------
    # Notification helpers
    # ------------------------------------------------------------------

    def notify_tracked(
        self,
        message: str,
        *,
        title: str = "",
        severity: SeverityLevel = "information",
        timeout: float | None = None,
        markup: bool = True,
    ) -> Notification:
        if timeout is None:
            timeout = self._actions.notification_timeout()
        notification = Notification(message, title, severity, timeout, markup=markup)
        self._actions.post_notification(notification)
        return notification

    def dismiss_notification(self, notification: Notification | None) -> None:
        if notification is None:
            return
        self._actions.unnotify(notification)

    # ------------------------------------------------------------------
    # Async command implementations
    # ------------------------------------------------------------------

    async def list_sessions_command(self) -> None:
        await self._actions.refresh_server_sessions(include_platform=True)
        self._actions.write_session_listing()

    async def reload_capabilities_command(self) -> None:
        runtime_info = await self.reload_capabilities_with_feedback()
        await self._actions.apply_runtime_info(runtime_info, refresh_skills=True)
        cap_count = len(runtime_info.capabilities)
        agent_count = sum(len(c.agents) for c in runtime_info.capabilities)
        self._actions.flash(
            f"Reloaded {cap_count} capabilities, {agent_count} agents",
            severity="success",
        )

    async def reload_capabilities_with_feedback(
        self,
        *,
        client: "ManagedRuntimeClient | None" = None,
    ) -> RuntimeInfo:
        reload_client = client or self._actions.local_runtime_client()
        # Route through the port so tests monkeypatching ``app._notify_tracked``
        # / ``app._dismiss_notification`` intercept the call.
        notification = self._actions.notify_tracked(
            "Reloading...", severity="information", timeout=10
        )
        self._actions.set_status("Reloading", busy=True)
        try:
            return await reload_client.reload_capabilities()
        finally:
            self._actions.dismiss_notification(notification)
            self._actions.set_status("Ready", busy=False)

    async def refresh_skill_names(self) -> None:
        """Fetch skill names for the slash overlay and dispatcher fallback.

        Each skill is registered by its qualified identifier so the displayed
        command does not mutate when neighboring capabilities load — the same
        stability invariant tools keep via always-qualified wire names. The
        dispatcher still accepts bare-unambiguous input per CAP-IDENT-017
        (see ``handle_command``); qualified display + bare-unambiguous input
        is the split.
        """
        self._actions.set_skill_names(set())
        try:
            skills = await self._actions.managed_client().fetch_skills()
            builtin = {c.name.lstrip("/") for c in SLASH_COMMANDS}
            entries: set[tuple[str, str]] = set()
            for s in skills:
                command = s.qualified_id or s.name
                if command in builtin:
                    continue
                entries.add((command, s.description))
            self._actions.set_skill_names(entries)
            logger.debug("Skills refresh | count={}", len(self._actions.skill_names()))
        except Exception:
            logger.opt(exception=True).debug("Failed to refresh skill names")

    async def whoami_command(self) -> None:
        if not self._actions.authenticated():
            self._actions.flash("Not logged in", severity="warning")
            return
        name, profile = self._actions.active_profile()
        if name is None or profile is None:
            self._actions.flash("Not logged in. Use /login first.", severity="warning")
            return
        self._actions.write_whoami(name=name, profile=profile)

    async def load_skill_command(self, name: str, extra: str = "") -> None:
        """Fetch rendered skill content and send it as a user message.

        Matches the OpenCode pattern of sending skill content as a plain
        user message rather than injecting it via a tool call.
        """
        try:
            content = await self._actions.managed_client().fetch_skill_content(name)
        except Exception:
            logger.opt(exception=True).warning("Failed to load skill | name={}", name)
            self._actions.flash(f"Skill '{name}' not found", severity="warning")
            return

        parts = [content]
        if extra.strip():
            parts.extend(["", extra.strip()])
        self._actions.send_chat("\n".join(parts))

    async def workspace_info_command(self) -> None:
        try:
            _name, profile = self._actions.active_profile()
        except Exception as exc:
            self._actions.flash(str(exc), severity="warning")
            return
        if profile is None:
            self._actions.flash("Not logged in. Use /login first.", severity="warning")
            return
        for label, value in [
            ("org", profile.default_organization),
            ("workspace", profile.default_workspace),
            ("project", profile.default_project),
        ]:
            if value:
                self._actions.write_activity(f"{label} {value}", style="info")

    async def switch_workspace_command(self, args: list[str]) -> None:
        import asyncio

        if not self._actions.authenticated():
            self._actions.flash(
                "Not authenticated — use /login to connect to the platform",
                severity="warning",
            )
            return
        if not args:
            self._actions.flash("Usage: /workspace <key>", severity="warning")
            return
        workspace_key = args[0]

        try:
            profile_name, profile = self._actions.active_profile()
        except Exception as exc:
            self._actions.flash(str(exc), severity="warning")
            return
        if profile_name is None or profile is None:
            self._actions.flash("Not logged in. Use /login first.", severity="warning")
            return

        org = profile.default_organization
        if not org:
            self._actions.flash("No organization configured. Use /login first.", severity="warning")
            return

        try:
            api, _profile = await asyncio.to_thread(self._actions.platform_client)
            workspace = await asyncio.to_thread(api.get_workspace, org, workspace_key)
        except Exception as exc:
            self._actions.flash(str(exc), severity="warning")
            return

        if workspace is None:
            self._actions.flash(f"Workspace not found: {workspace_key}", severity="error")
            return

        if profile.default_workspace == workspace_key:
            self._actions.flash(f"Already on workspace: {workspace_key}", severity="info")
            return

        default_project = await asyncio.to_thread(api.get_default_project_key, org, workspace_key)
        updated_profile = profile.model_copy(
            update={
                "default_workspace": workspace_key,
                "default_project": default_project,
            }
        )

        try:
            await asyncio.to_thread(self._actions.save_profile, profile_name, updated_profile)
        except Exception as exc:
            self._actions.flash(f"Failed to save profile: {exc}", severity="error")
            return

        await self._actions.profile_manager_apply_auth_profile(updated_profile)
        self._actions.flash(
            f"Switched to workspace: {workspace.name} — sessions cleared",
            severity="success",
        )

    async def workspaces_command(self) -> None:
        import asyncio

        api, profile = await asyncio.to_thread(self._actions.platform_client)
        workspaces = await asyncio.to_thread(api.list_workspaces, profile.default_organization)
        if not workspaces:
            self._actions.flash("No workspaces found", severity="warning")
            return
        for ws in workspaces:
            is_active = ws.key == profile.default_workspace
            marker = " \u2190 active" if is_active else ""
            default_marker = " (default)" if ws.is_default else ""
            self._actions.write_activity(
                f"{ws.key} \u00b7 {ws.name}{marker}{default_marker}",
                style="success" if is_active else "info",
            )

    async def projects_command(self, args: list[str] | None = None) -> None:
        import asyncio

        api, profile = await asyncio.to_thread(self._actions.platform_client)
        org = profile.default_organization
        workspace = args[0] if args else profile.default_workspace
        if not org or not workspace:
            self._actions.flash("No org/workspace. Use /login first.", severity="warning")
            return
        projects = await asyncio.to_thread(api.list_projects, org, workspace)
        if not projects:
            self._actions.flash("No projects found", severity="warning")
            return
        for p in projects:
            self._actions.write_activity(f"{p.key} \u00b7 {p.name}", style="info")

    async def models_command(self) -> None:
        import asyncio

        api, profile = await asyncio.to_thread(self._actions.platform_client)
        models = await asyncio.to_thread(api.list_models, profile.default_organization)
        if not models:
            self._actions.flash("No models found", severity="warning")
            return
        for m in models:
            self._actions.write_activity(
                f"{m.name} \u00b7 {m.latest_version or 'n/a'}", style="info"
            )

    async def pull_command(self, raw_ref: str) -> None:
        import asyncio

        api, profile = await asyncio.to_thread(self._actions.platform_client)
        scheme, parsed = self._actions.parse_pull_ref(raw_ref, default_org=profile.org_key)

        version_suffix = f":{parsed.version}" if parsed.version else ""
        package_ref = f"{scheme}://{parsed.qualified_name}{version_suffix}"
        storage = self._actions.make_storage(profile=profile, api=api)
        result = await asyncio.to_thread(self._actions.package_pull, package_ref, _storage=storage)

        if not result.success:
            raise RuntimeError("; ".join(result.errors) or "Pull failed")

        resolved_version = result.version or parsed.version or "latest"
        display_ref = f"{parsed.qualified_name}@{resolved_version}"
        if result.dest is not None:
            self._actions.flash(f"Pulled {display_ref} to {result.dest}", severity="success")
            return

        self._actions.flash(f"Already available locally: {display_ref}", severity="info")
