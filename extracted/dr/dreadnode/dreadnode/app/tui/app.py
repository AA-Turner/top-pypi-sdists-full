import asyncio
import contextlib
import json
import re
import time
import typing as t
from dataclasses import dataclass
from pathlib import Path

from textual import events, on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.css.query import NoMatches
from textual.notifications import Notification, Notify, SeverityLevel
from textual.reactive import reactive
from textual.theme import Theme
from textual.widgets import Static, TextArea

from dreadnode.app.api.client import AuthenticationError
from dreadnode.app.api.models import HumanInputResponse, HumanPrompt, QuestionAnswer
from dreadnode.app.cli.args import RESUME_PICK_SENTINEL
from dreadnode.app.cli.shared import ArtifactRef
from dreadnode.app.client.managed_client import ManagedRuntimeClient
from dreadnode.app.client.models import CapabilityInfo, RuntimeInfo, SessionInfo
from dreadnode.app.client.runtime_client import DEFAULT_MODEL
from dreadnode.app.config import DEFAULT_PLATFORM_URL, Profile, UserConfig
from dreadnode.app.server.runtime_events import (
    EVENT_COMPONENT_STATE_CHANGED,
    RuntimeEventEnvelope,
)
from dreadnode.app.tui.auth_flow import (
    _active_profile,
    _active_profile_name,
    _clear_in_memory_profile,
    _delete_profile,
    _disconnect_profile,
    _platform_client,
    _save_profile,
    _set_in_memory_profile,
)
from dreadnode.app.tui.capabilities_manager import (
    CapabilitiesManager,
    CapabilitiesSummary,
    ComponentStateChanged,
)
from dreadnode.app.tui.command_dispatcher import CommandDispatcher
from dreadnode.app.tui.commands import SlashCommand
from dreadnode.app.tui.error_handler import (
    ErrorHandler,
)
from dreadnode.app.tui.model_manager import ModelCatalogState, ModelManager
from dreadnode.app.tui.profile_manager import ProfileFlowState, ProfileManager
from dreadnode.app.tui.screen_router import ScreenRouter
from dreadnode.app.tui.sessions_manager import (
    SessionRecord,
    SessionsManager,
)
from dreadnode.app.tui.turn_coordinator import TurnCoordinator
from dreadnode.packaging.package import Package
from dreadnode.storage.storage import Storage

if t.TYPE_CHECKING:
    from rich.text import Text as RichText
    from textual.events import Key
    from textual.screen import Screen
    from textual.widget import Widget

    from dreadnode.app.tui.connection import SessionStateBundle
    from dreadnode.app.tui.screens.workspaces import SwitchRequest

from loguru import logger

from dreadnode.app.tui.status_messages import STATUS_READY, STATUS_STARTING
from dreadnode.app.tui.theme import (
    ACCENT,
    BG,
    BRAND,
    ERROR,
    FG,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    INFO,
    SUCCESS,
    WARNING,
)
from dreadnode.app.tui.turn_lifecycle import TurnLifecycle
from dreadnode.app.tui.turn_lifecycle import TurnPhase as LifecyclePhase
from dreadnode.app.tui.turn_reducer import TurnState
from dreadnode.app.tui.widgets import (
    ConversationView,
    Flash,
    HumanPromptWidget,
    MentionOverlay,
    MessageQueue,
    NewMessagesPill,
    SlashOverlay,
    StreamingDraft,
    ToolProgress,
    Welcome,
    render_help,
)
from dreadnode.app.tui.widgets.agent_dialog import AgentDialog
from dreadnode.app.tui.widgets.composer import ComposerInput
from dreadnode.app.tui.widgets.context_bar import ContextBar, PageStatus
from dreadnode.app.tui.widgets.profile_dialog import ProfileDialog
from dreadnode.app.tui.widgets.rewind_picker import RewindCandidate, RewindPickerOverlay
from dreadnode.app.tui.widgets.skills_dialog import SkillsDialog
from dreadnode.app.tui.widgets.status_bar import StatusBar
from dreadnode.app.tui.widgets.tools_dialog import ToolsDialog
from dreadnode.core.log import enable_tui_capture, install_stdlib_intercept
from dreadnode.generators.message import Message

_MAX_HISTORY = 500
_HISTORY_FILE = Path.home() / ".dreadnode" / "prompt-history.jsonl"
_PULLABLE_PACKAGE_SCHEMES = ("capability", "dataset", "model", "environment")


def _coerce_policy_arg(raw: str) -> t.Any:
    """Coerce a ``/policy k=v`` value token into its best-fit Python type.

    Integers and floats become ``int``/``float``. ``true`` / ``false``
    (case-insensitive) become ``bool``. Everything else stays a
    string. Keeps the slash command ergonomic — users don't need to
    remember which policy params are strings vs ints.
    """
    lower = raw.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    return raw


def _parse_tui_pull_ref(raw: str, *, default_org: str) -> tuple[str, ArtifactRef]:
    """Parse a typed Hub artifact ref into a package scheme and normalized artifact ref."""
    value = raw.strip()
    if not value:
        raise ValueError("Usage: /pull <type://[org/]name[@version]>")

    if "://" not in value:
        raise ValueError(
            "Pull refs must include a type prefix like dataset://, model://, capability://, or environment://"
        )

    scheme, artifact = value.split("://", 1)
    scheme = scheme.strip().lower()
    artifact = artifact.strip()

    if scheme == "task":
        raise ValueError("Use environment:// for task packages")

    if scheme not in _PULLABLE_PACKAGE_SCHEMES:
        allowed = ", ".join(_PULLABLE_PACKAGE_SCHEMES)
        raise ValueError(f"Unknown pull type '{scheme}'. Valid types: {allowed}")

    leaf = artifact.rsplit("/", 1)[-1]
    if ":" in leaf and "@" not in leaf:
        base, version = artifact.rsplit(":", 1)
        artifact = f"{base}@{version}"

    return scheme, ArtifactRef.parse(artifact, default_org)


def _shorten_model(model: str) -> str:
    """Reduce a fully-qualified model id to its leaf for compact display."""
    return model.rsplit("/", 1)[-1] if "/" in model else model


# Upper bound on the agent-name column in the ``/agents`` listing. The column
# grows to fit the longest name present, but never past this — so one very long
# name can't push every description off-screen. Names are never truncated; a
# name longer than this takes its own line (see ``_build_agent_listing``).
_AGENT_NAME_COL_MAX = 32


def _build_agent_listing(capabilities: list[CapabilityInfo], active_agent: str) -> "list[RichText]":
    """Build the inline ``/agents`` listing, grouped by capability.

    Pure (Rich-only, no Textual/app state) so it can be unit-tested directly.
    Agents are grouped under a per-capability header instead of repeating the
    capability inline, which keeps names and categories from running together.
    """
    from rich.text import Text as RichText

    all_agents = [a for c in capabilities for a in c.agents]
    header = RichText()
    header.append("· ", style=INFO)
    header.append(f"Agents ({len(all_agents)})", style=f"bold {INFO}")
    lines: list[RichText] = [header]

    # One global name column so descriptions line up down the whole list,
    # sized to the longest name but capped (see ``_AGENT_NAME_COL_MAX``). A name
    # within the column is padded so its description aligns; a name past the cap
    # takes its own line and drops its description to an aligned line below.
    width = min(max((len(a.name) for a in all_agents), default=0), _AGENT_NAME_COL_MAX)
    desc_indent = " " * (6 + width + 2)  # "    ○ " (6) + name column + 2 gutter

    for cap in capabilities:
        if not cap.agents:
            continue

        # Blank line above each heading to set the groups apart.
        lines.append(RichText())
        cap_header = RichText()
        cap_header.append("  ")
        cap_header.append(cap.display_name or cap.name, style=f"bold {FG_SUBTLE}")
        lines.append(cap_header)

        for a in cap.agents:
            is_active = a.name == active_agent
            name_style = f"bold {FG}" if is_active else FG

            # Description + optional model, as styled spans, built once.
            detail = RichText()
            desc = a.description.strip()
            if desc:
                if len(desc) > 60:
                    desc = desc[:57] + "…"
                detail.append(desc, style=FG_MUTED)
            if a.model and a.model != "inherit":
                if detail.plain:
                    detail.append("  ")
                detail.append(_shorten_model(a.model), style=FG_FAINTEST)

            line = RichText()
            marker = "●" if is_active else "○"
            line.append(f"    {marker} ", style=ACCENT if is_active else FG_FAINTEST)

            if len(a.name) <= width:
                # Fits the column — pad so the detail aligns on the same line.
                line.append(f"{a.name:<{width}}", style=name_style)
                if detail.plain:
                    line.append("  ")
                    line.append_text(detail)
                lines.append(line)
            else:
                # Overflows — the full name takes this line; align the detail
                # on a continuation line so it never gets pushed off-screen.
                line.append(a.name, style=name_style)
                lines.append(line)
                if detail.plain:
                    cont = RichText()
                    cont.append(desc_indent)
                    cont.append_text(detail)
                    lines.append(cont)

    # Footer hint — the listing is read-only, so point at the ways to act on it.
    hint = RichText()
    hint.append("  Switch with ", style=FG_FAINTEST)
    hint.append("/agent <name>", style=FG_MUTED)
    hint.append(" or press ", style=FG_FAINTEST)
    hint.append("Ctrl+A", style=FG_MUTED)
    lines.append(hint)

    return lines


@dataclass(slots=True)
class _AppProxyModelView:
    _app: "DreadnodeTextualApp"

    def current_model(self) -> str:
        return self._app.model

    def platform_model_ids(self) -> list[str]:
        return self._app._model_manager.platform_model_ids()


@dataclass(slots=True)
class _AppWarningSink:
    _app: "DreadnodeTextualApp"

    def flash_warning(self, message: str) -> None:
        self._app._flash(message, severity="warning")


@dataclass(slots=True)
class _AppProxyAuthActions:
    _app: "DreadnodeTextualApp"

    def reauthenticate_proxy(self) -> None:
        self._app._run_command(self._app._model_manager.provision_litellm_key)


@dataclass(slots=True)
class _AppModelCatalogContext:
    _app: "DreadnodeTextualApp"

    def current_model(self) -> str:
        return self._app.model

    def is_authenticated(self) -> bool:
        return self._app.authenticated

    def current_profile(self) -> Profile | None:
        return self._app._current_profile

    def platform_client(self) -> tuple[t.Any, Profile]:
        return _platform_client()

    def current_org(self) -> str | None:
        return self._app._connection_manager._org

    def model_was_explicitly_selected(self) -> bool:
        return self._app._model_explicitly_set


@dataclass(slots=True)
class _AppModelUiHost:
    _app: "DreadnodeTextualApp"

    def model_browser_open(self) -> bool:
        from dreadnode.app.tui.screens import ModelBrowserScreen

        with contextlib.suppress(Exception):
            return self._app._is_screen_open(ModelBrowserScreen)
        return False

    def dismiss_pushed_screens(self) -> None:
        self._app._dismiss_pushed_screens()

    def open_model_browser(
        self,
        *,
        platform_models: list[dict[str, t.Any]],
        byok_models: list[dict[str, t.Any]],
        current_model: str,
        inference_credits_per_dollar: int | None,
        access_restricted: bool,
        search_models: t.Callable[..., t.Any],
        on_selected: t.Callable[[str | None], None],
    ) -> None:
        from dreadnode.app.tui.screens import ModelBrowserScreen

        self._app.push_screen(
            ModelBrowserScreen(
                platform_models=platform_models,
                byok_models=byok_models,
                current_model=current_model,
                inference_credits_per_dollar=inference_credits_per_dollar,
                access_restricted=access_restricted,
                search_models=search_models,
            ),
            callback=on_selected,
        )

    def refresh_model_browser(
        self,
        *,
        platform_models: list[dict[str, t.Any]],
        byok_models: list[dict[str, t.Any]],
        current_model: str,
        inference_credits_per_dollar: int | None,
        access_restricted: bool,
    ) -> None:
        from dreadnode.app.tui.screens import ModelBrowserScreen

        with contextlib.suppress(Exception):
            for screen in self._app.screen_stack:
                if isinstance(screen, ModelBrowserScreen):
                    screen.set_models(
                        platform_models=platform_models,
                        byok_models=byok_models,
                        current_model=current_model,
                        inference_credits_per_dollar=inference_credits_per_dollar,
                        access_restricted=access_restricted,
                    )
                    break


@dataclass(slots=True)
class _AppModelRunner:
    _app: "DreadnodeTextualApp"

    def run_exclusive(self, coro: t.Awaitable[t.Any], *, group: str) -> None:
        self._app.run_worker(
            coro,
            exit_on_error=False,
            exclusive=True,
            group=group,
        )


@dataclass(slots=True)
class _AppModelNotifier:
    _app: "DreadnodeTextualApp"

    def flash_info(self, message: str) -> None:
        self._app._flash(message, severity="info")

    def flash_warning(self, message: str) -> None:
        self._app._flash(message, severity="warning")


@dataclass(slots=True)
class _AppModelSelectionActions:
    _app: "DreadnodeTextualApp"

    def apply_model(self, model_id: str) -> None:
        self._app._on_model_changed(model_id)

    def persist_default_model_choice(self, model_id: str) -> None:
        self._app._run_command(self._app._persist_default_model_choice, model_id)

    def mark_model_explicitly_selected(self) -> None:
        self._app._model_explicitly_set = True


@dataclass(slots=True)
class _AppScreenHost:
    _app: "DreadnodeTextualApp"

    def is_screen_open(self, screen_type: type[object]) -> bool:
        return self._app._is_screen_open(screen_type)

    def dismiss_pushed_screens(self) -> None:
        self._app._dismiss_pushed_screens()

    def push_screen(
        self,
        screen: object,
        callback: t.Callable[[t.Any], None] | None = None,
    ) -> None:
        self._app.push_screen(t.cast("Screen[t.Any]", screen), callback=callback)


@dataclass(slots=True)
class _AppSessionView:
    _app: "DreadnodeTextualApp"

    def sessions_snapshot(self) -> dict[str, SessionRecord]:
        return dict(self._app.sessions)

    def active_session_id(self) -> str | None:
        return self._app.active_session_id


@dataclass(slots=True)
class _AppRuntimeView:
    _app: "DreadnodeTextualApp"

    def runtime_info(self) -> RuntimeInfo | None:
        return self._app.runtime_info

    def runtime_client(self) -> ManagedRuntimeClient:
        return self._app.managed_client

    def connection_manager(self) -> t.Any:
        return self._app._connection_manager


@dataclass(slots=True)
class _AppScreenRouterActions:
    _app: "DreadnodeTextualApp"

    def on_session_picked(self, result: str | None) -> None:
        self._app._on_session_picked(result)

    def refresh_sessions_then_open_picker(self) -> None:
        self._app._refresh_sessions_then_open_picker()

    def on_workspace_screen_dismiss(self, result: "SwitchRequest | None") -> None:
        self._app._on_workspace_screen_dismiss(result)

    def on_capabilities_dismiss(self, result: t.Any) -> None:
        self._app._on_capabilities_dismiss(result)

    def collect_mcp_servers(self) -> list[dict[str, t.Any]]:
        return self._app._capabilities_manager.collect_mcp_servers()

    def collect_workers(self) -> list[dict[str, t.Any]]:
        return self._app._capabilities_manager.collect_workers()

    def flash_warning(self, message: str) -> None:
        self._app._flash(message, severity="warning")

    def handle_authentication_error(self, message: str) -> None:
        self._app._profile_manager.handle_authentication_error(message)

    def consume_pending_capability_reload(self) -> bool:
        return self._app._capabilities_manager.consume_pending_capability_reload()

    def reload_and_open_capabilities(self) -> None:
        self._app._run_command(self._app._capabilities_manager.reload_and_open)

    def save_default_project(self, project_key: str) -> None:
        current_profile = self._app._current_profile
        if current_profile is None or not current_profile.name:
            return
        current_profile.default_project = project_key
        user_config = UserConfig.read()
        user_config.save_profile(current_profile)
        user_config.write()


@dataclass(slots=True)
class _AppProfileState:
    _app: "DreadnodeTextualApp"

    def current_profile(self) -> Profile | None:
        return self._app._current_profile

    def set_current_profile(self, profile: Profile) -> None:
        self._app._current_profile = profile

    def server_url(self) -> str:
        return self._app._server_url

    def update_available(self) -> str:
        return self._app.update_available

    def set_authenticated(self, value: bool) -> None:
        self._app.authenticated = value

    def set_runtime_connected(self, value: bool) -> None:
        self._app.runtime_connected = value

    def set_model(self, model_id: str) -> None:
        self._app.model = model_id
        self._app.model_name = model_id

    def resume_session_id(self) -> str | None:
        return self._app._resume_session_id

    def active_session_id(self) -> str | None:
        return self._app.active_session_id

    def set_active_session_id(self, session_id: str | None) -> None:
        self._app.active_session_id = session_id

    def consume_initial_inputs(
        self,
    ) -> tuple[str | None, str | None, dict[str, t.Any] | None]:
        initial_agent = self._app._initial_agent
        initial_prompt = self._app._initial_prompt
        initial_policy = self._app._initial_policy
        self._app._initial_agent = None
        self._app._initial_prompt = None
        self._app._initial_policy = None
        return initial_agent, initial_prompt, initial_policy


@dataclass(slots=True)
class _AppProfileUi:
    _app: "DreadnodeTextualApp"

    def flash(self, message: str, *, severity: str) -> None:
        self._app._flash(message, severity=severity)

    def write_activity(self, message: str, *, style: str = "info") -> None:
        self._app._write_activity(message, style=style)

    def set_status(self, text: str, *, busy: bool | None = None) -> None:
        self._app._set_status(text, busy=busy)

    def set_boot_status(self, text: str) -> None:
        self._app._set_boot_status(text)

    def set_connection_status(self, text: str) -> None:
        self._app._set_connection_status(text)

    def set_composer_enabled(self, enabled: bool) -> None:
        self._app._set_composer_enabled(enabled)

    def sync_conversation(self) -> None:
        self._app._sync_conversation()

    def update_context(self) -> None:
        self._app._update_context()

    def dismiss_welcome(self) -> None:
        self._app._dismiss_welcome()


@dataclass(slots=True)
class _AppProfileScreen:
    _app: "DreadnodeTextualApp"

    def profile_dialog_visible(self) -> bool:
        with contextlib.suppress(Exception):
            dialog = self._app.query_one("#profile-dialog", ProfileDialog)
            return dialog.is_visible
        return False

    def hide_profile_dialog(self) -> None:
        with contextlib.suppress(Exception):
            self._app.query_one("#profile-dialog", ProfileDialog).hide()

    def show_profile_dialog(
        self,
        servers: dict[str, Profile],
        active_name: str | None,
    ) -> None:
        dialog = self._app.query_one("#profile-dialog", ProfileDialog)
        dialog.show_profiles(servers, active_name)

    def dismiss_pushed_screens(self) -> None:
        self._app._dismiss_pushed_screens()

    def current_screen(self) -> object:
        return self._app.screen

    def push_screen(
        self,
        screen: object,
        callback: t.Callable[[t.Any], None] | None = None,
    ) -> None:
        self._app.push_screen(t.cast("Screen[t.Any]", screen), callback=callback)

    def focus_composer(self) -> None:
        self._app.query_one("#composer", ComposerInput).focus()

    def exit_app(self) -> None:
        self._app.exit()

    def update_auth_banner(self, banner: str) -> None:
        from dreadnode.app.tui.screens.auth import AuthModal

        screen = self._app.screen
        if isinstance(screen, AuthModal):
            screen.query_one("#auth-update-banner", Static).update(f"[bold yellow]{banner}[/]")


@dataclass(slots=True)
class _AppProfileRuntime:
    _app: "DreadnodeTextualApp"

    def set_api_context(self, api: t.Any, organization: str, workspace: str) -> None:
        self._app._connection_manager.set_api_context(api, organization, workspace)

    def set_platform_profile(self, profile: Profile) -> None:
        self._app._connection_manager.local_client.set_platform_profile(profile)

    def clear_platform_profile(self) -> None:
        self._app._connection_manager.local_client.clear_platform_profile()

    def local_runtime_started(self) -> bool:
        return self._app._connection_manager.local_client.is_started

    async def start_local_runtime(self) -> None:
        await self._app._connection_manager.local_client.start()

    async def restart_local_runtime(self) -> None:
        await self._app._connection_manager.local_client.restart()

    async def refresh_runtime(self) -> None:
        await self._app._capabilities_manager.refresh()

    async def refresh_server_sessions(self, *, include_platform: bool = False) -> None:
        await self._app._refresh_server_sessions(include_platform=include_platform)

    async def refresh_skill_names(self) -> None:
        await self._app._command_dispatcher.refresh_skill_names()

    async def resume_requested_session(self) -> None:
        await self._app._resume_requested_session()

    async def create_new_session(
        self,
        agent: str | None = None,
        *,
        policy: dict[str, t.Any] | None = None,
    ) -> None:
        await self._app._create_new_session_impl(agent, policy=policy)

    def send_chat(self, message: str) -> None:
        self._app._send_chat(message)

    def collect_agents(self) -> list[dict[str, str]]:
        return self._app._capabilities_manager.collect_agents()


@dataclass(slots=True)
class _AppProfileModels:
    _app: "DreadnodeTextualApp"

    def clear_platform_proxy_state(self) -> None:
        self._app._model_manager.clear_platform_proxy_state()

    async def refresh_platform_models_and_key(self, api: t.Any) -> None:
        await self._app._model_manager.refresh_platform_models_and_key(api)

    def model_from_profile(self, profile: Profile | None) -> str:
        return self._app._model_from_profile(profile)


class _AppProfileStore:
    def read_user_config(self) -> UserConfig:
        return UserConfig.read()

    def active_profile_name(self) -> str | None:
        return _active_profile_name()

    def delete_profile(self, profile_name: str) -> bool:
        return _delete_profile(profile_name)

    def activate_profile(self, profile_name: str) -> None:
        config = UserConfig.read()
        config.activate(profile_name)
        config.write()

    def save_profile(self, profile: Profile) -> None:
        config = UserConfig.read()
        config.save_profile(profile)
        config.write()

    def set_in_memory_profile(self, profile_name: str | None, profile: Profile) -> None:
        _set_in_memory_profile(profile_name, profile)

    def clear_in_memory_profile(self) -> None:
        _clear_in_memory_profile()

    def active_profile(self) -> tuple[str | None, Profile | None]:
        return _active_profile()

    def disconnect_profile(self) -> str | None:
        return _disconnect_profile()


@dataclass(slots=True)
class _AppProfileAsyncActions:
    _app: "DreadnodeTextualApp"

    def run_exclusive(self, coro: t.Awaitable[t.Any], *, group: str) -> None:
        self._app.run_worker(
            coro,
            exit_on_error=False,
            exclusive=True,
            group=group,
        )

    def run_command(
        self,
        func: t.Callable[..., t.Awaitable[t.Any]],
        *args: t.Any,
    ) -> None:
        self._app._run_command(func, *args)


# ─────────────────────────────────────────────────────────────────────────────
# SessionsManager adapters
# ─────────────────────────────────────────────────────────────────────────────
#
# These wrap the app to implement the three narrow ports that
# :class:`SessionsManager` depends on. Nothing in the manager itself knows
# about ``DreadnodeTextualApp`` — the split keeps session event handling
# testable without spinning up a live Textual app.


@dataclass(slots=True)
class _AppSessionsUi:
    _app: "DreadnodeTextualApp"

    def query_draft(self) -> StreamingDraft:
        return self._app.query_one("#draft", StreamingDraft)

    def query_composer(self) -> ComposerInput:
        return self._app.query_one("#composer", ComposerInput)

    def query_conversation(self) -> ConversationView:
        return self._app.query_one("#conversation", ConversationView)

    def query_prompt_widget(self) -> HumanPromptWidget:
        return self._app.query_one("#human-prompt", HumanPromptWidget)

    def query_tool_progress(self) -> ToolProgress:
        return self._app.query_one("#tool-progress", ToolProgress)

    def query_message_queue(self) -> MessageQueue:
        return self._app.query_one("#message-queue", MessageQueue)

    def call_after_refresh(
        self,
        callback: t.Callable[..., t.Any],
        /,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> None:
        self._app.call_after_refresh(callback, *args, **kwargs)

    def flash(self, message: str, *, severity: str = "info") -> None:
        self._app._flash(message, severity=severity)

    def write_activity(self, message: str, *, style: str = "info") -> None:
        self._app._write_activity(message, style=style)

    def set_composer_enabled(self, enabled: bool) -> None:
        self._app._set_composer_enabled(enabled)

    def append_transcript(
        self,
        entry: Message,
        session_id: str,
        **kwargs: t.Any,
    ) -> None:
        # Delegates at call time so tests that patch
        # ``app._append_transcript = MagicMock()`` still intercept the call
        # when the manager dispatches an event. ``**kwargs`` is used so the
        # default ``scroll=True`` call arrives at the mock without an
        # explicit ``scroll=True`` kwarg (matching the pre-refactor shape
        # the tests assert against).
        self._app._append_transcript(entry, session_id, **kwargs)


@dataclass(slots=True)
class _AppSessionsContext:
    _app: "DreadnodeTextualApp"

    def active_session_id(self) -> str | None:
        return self._app.active_session_id

    def set_active_session_id(self, session_id: str | None) -> None:
        self._app.active_session_id = session_id

    def update_context(self) -> None:
        self._app._update_context()

    def last_input_tokens(self) -> int:
        return self._app.last_input_tokens

    def set_last_input_tokens(self, tokens: int) -> None:
        self._app.last_input_tokens = tokens

    def tool_call_count(self) -> int:
        return self._app.tool_call_count

    def set_tool_call_count(self, count: int) -> None:
        self._app.tool_call_count = count

    def cost_usd(self) -> float:
        return self._app.cost_usd

    def set_cost_usd(self, cost: float) -> None:
        self._app.cost_usd = cost

    def cost_unknown(self) -> bool:
        return self._app.cost_unknown

    def set_cost_unknown(self, unknown: bool) -> None:
        self._app.cost_unknown = unknown

    def subagent_cost_usd(self) -> float:
        return self._app.subagent_cost_usd

    def set_subagent_cost_usd(self, cost: float) -> None:
        self._app.subagent_cost_usd = cost

    def show_thinking(self) -> bool:
        return self._app._show_thinking

    def authenticated(self) -> bool:
        return self._app.authenticated

    def current_model(self) -> str:
        return self._app.model

    def apply_model_change(self, model: str) -> None:
        self._app._on_model_changed(model)

    def turn_enter_awaiting(self, status: str) -> None:
        self._app._turn.enter_awaiting(status)

    def turn_sync_projection(
        self,
        *,
        owner: str | None,
        phase: LifecyclePhase,
        status: str,
        authenticated: bool,
    ) -> None:
        self._app._turn.sync_projection(
            owner=owner,
            phase=phase,
            status=status,
            authenticated=authenticated,
        )

    def report_url(self, session_id: str) -> str | None:
        return self._app._build_monitoring_url(session_id, view="reports")

    def agent_output_url(self, project: str | None) -> str | None:
        return self._app._build_agent_output_url(project)


@dataclass(slots=True)
class _AppSessionsTransport:
    """Narrow view of the runtime ``managed_client`` for the sessions manager.

    Delegates to whichever ``managed_client`` is currently active (local or
    remote) at call time so the subscription policy automatically tracks
    runtime switches.
    """

    _app: "DreadnodeTextualApp"

    def is_runtime_started(self) -> bool:
        return bool(getattr(self._app.managed_client, "is_started", True))

    def desired_session_subscriptions(self) -> set[str]:
        return self._app.managed_client.desired_session_subscriptions()

    async def subscribe_session(self, session_id: str) -> None:
        await self._app.managed_client.subscribe_session(session_id)

    async def unsubscribe_session(self, session_id: str) -> None:
        await self._app.managed_client.unsubscribe_session(session_id)

    def latest_session_snapshot(self, session_id: str) -> dict[str, t.Any] | None:
        snapshot_fn = getattr(self._app.managed_client, "latest_session_snapshot", None)
        return snapshot_fn(session_id) if callable(snapshot_fn) else None

    def latest_session_resync_required(self, session_id: str) -> dict[str, t.Any] | None:
        resync_fn = getattr(self._app.managed_client, "latest_session_resync_required", None)
        return resync_fn(session_id) if callable(resync_fn) else None

    async def fetch_session_messages(self, session_id: str) -> list[dict[str, t.Any]]:
        return await self._app.managed_client.fetch_session_messages(session_id)

    async def list_sessions(self, *, include_platform: bool = False) -> list[SessionInfo]:
        return await self._app.managed_client.list_sessions(include_platform=include_platform)

    async def get_session(self, session_id: str) -> SessionInfo | None:
        return await self._app.managed_client.get_session(session_id)


@dataclass(slots=True)
class _AppSessionsModelAccess:
    _app: "DreadnodeTextualApp"

    def refresh_platform_model_access(self) -> None:
        try:
            api, _profile = _platform_client()
        except Exception:
            logger.debug("Cannot refresh platform model access: no platform client available")
            return
        self._app._run_command(self._app._model_manager.refresh_platform_models_and_key, api)


# ─────────────────────────────────────────────────────────────────────────────
# CommandDispatcher adapter
# ─────────────────────────────────────────────────────────────────────────────
#
# :class:`CommandDispatcher` takes one fat ``CommandActions`` port and does
# all its routing through it. The adapter maps each port method to whatever
# piece of the app (its own methods, another manager, a reactive) owns
# that behavior. Methods delegate at call time so tests that patch
# ``app._X = MagicMock()`` still intercept calls coming from inside the
# dispatcher.


@dataclass(slots=True)
class _AppCommandActions:
    _app: "DreadnodeTextualApp"

    # ------------------------------------------------------------------
    # Status, flash, activity
    # ------------------------------------------------------------------

    def flash(self, message: str, *, severity: str = "info") -> None:
        self._app._flash(message, severity=severity)

    def write_activity(self, message: str, *, style: str = "info") -> None:
        self._app._write_activity(message, style=style)

    def set_status(self, text: str, *, busy: bool | None = None) -> None:
        self._app._set_status(text, busy=busy)

    def dismiss_welcome(self) -> None:
        self._app._dismiss_welcome()

    def show_help(self) -> None:
        self._app._show_help()

    def copy_last_assistant(self) -> None:
        self._app._copy_last_assistant()

    def write_session_listing(self) -> None:
        self._app._write_session_listing()

    def write_agent_listing(self) -> None:
        self._app._write_agent_listing()

    def write_whoami(self, *, name: str, profile: Profile) -> None:
        from dreadnode.app.tui.widgets.whoami import WhoAmI

        self._app._dismiss_welcome()
        widget = WhoAmI(
            name,
            profile.url,
            username=profile.username,
            email=profile.email,
            organization=profile.default_organization,
            workspace=profile.default_workspace,
            project=profile.default_project,
            classes="entry",
        )
        conv = self._app.query_one("#conversation", ConversationView)
        self._app.call_after_refresh(conv.append_entry_widget, widget)

    def post_notification(self, notification: Notification) -> None:
        self._app.post_message(Notify(notification))

    def unnotify(self, notification: Notification) -> None:
        self._app._unnotify(notification)

    def notification_timeout(self) -> float:
        return self._app.NOTIFICATION_TIMEOUT

    def notify_tracked(
        self,
        message: str,
        **kwargs: t.Any,
    ) -> Notification:
        # Delegates at call time so tests that monkeypatch
        # ``app._notify_tracked`` intercept the call coming from the
        # dispatcher (for example via ``reload_capabilities_with_feedback``).
        # ``**kwargs`` passes through only the explicitly-provided
        # keyword arguments so the mock sees exactly the caller's signature.
        return self._app._notify_tracked(message, **kwargs)

    def dismiss_notification(self, notification: Notification | None) -> None:
        self._app._dismiss_notification(notification)

    # ------------------------------------------------------------------
    # Reactive state
    # ------------------------------------------------------------------

    def authenticated(self) -> bool:
        return self._app.authenticated

    def current_model(self) -> str:
        return self._app.model

    def on_model_changed(self, model_id: str) -> None:
        self._app._on_model_changed(model_id)

    def thinking_enabled(self) -> bool:
        return self._app.thinking_enabled

    def set_thinking_enabled(self, value: bool) -> None:
        self._app.thinking_enabled = value

    def effort_label(self) -> str:
        return self._app.effort_label

    def set_effort_label(self, value: str) -> None:
        self._app.effort_label = value

    def set_show_thinking(self, value: bool) -> None:
        self._app._show_thinking = value

    def model_variants(self) -> dict[str, str]:
        return self._app._model_variants

    def set_skill_names(self, skill_names: set[tuple[str, str]]) -> None:
        self._app._skill_names = skill_names

    def skill_names(self) -> set[tuple[str, str]]:
        return self._app._skill_names

    def current_profile(self) -> Profile | None:
        return self._app._current_profile

    def set_current_profile(self, profile: Profile) -> None:
        self._app._current_profile = profile

    # ------------------------------------------------------------------
    # Runtime transport
    # ------------------------------------------------------------------

    def managed_client(self) -> ManagedRuntimeClient:
        return self._app.managed_client

    def local_runtime_client(self) -> ManagedRuntimeClient:
        return self._app._connection_manager.local_client

    # ------------------------------------------------------------------
    # Async command runner and orchestration
    # ------------------------------------------------------------------

    def run_command(
        self,
        coro_fn: t.Callable[..., t.Awaitable[t.Any]],
        *args: t.Any,
    ) -> None:
        self._app._run_command(coro_fn, *args)

    async def refresh_server_sessions(self, *, include_platform: bool = False) -> None:
        await self._app._refresh_server_sessions(include_platform=include_platform)

    async def apply_runtime_info(
        self,
        runtime_info: RuntimeInfo,
        *,
        refresh_skills: bool,
    ) -> None:
        await self._app._capabilities_manager.apply_runtime_info(
            runtime_info, refresh_skills=refresh_skills
        )

    def start_agent_session(self, agent_name: str) -> None:
        self._app._start_agent_session(agent_name)

    def send_chat(self, message: str) -> None:
        self._app._send_chat(message)

    def create_new_session(self, agent: str | None = None) -> None:
        if agent is None:
            agent = self._app._selected_agent_for_new_session()
        self._app._create_new_session(agent)

    def rename_session(self, title: str) -> None:
        self._app._rename_session(title)

    def export_session(self, filename: str | None) -> None:
        self._app._export_session(filename)

    async def set_session_policy_command(self, args: list[str], policy_name: str) -> None:
        await self._app._set_session_policy_command(args, policy_name)

    async def policy_command(self, args: list[str]) -> None:
        await self._app._policy_command(args)

    async def launch_background_task_command(self, args: list[str]) -> None:
        await self._app._launch_background_task_command(args)

    def handle_authentication_error(self, message: str) -> None:
        self._app._profile_manager.handle_authentication_error(message)

    async def update_command_body(self) -> None:
        await self._app._update_command()

    async def compact_command_body(self, args: list[str]) -> None:
        await self._app._compact_command(args)

    async def rewind_command_body(self) -> None:
        await self._app._rewind_command()

    def open_skills_dialog(self) -> None:
        self._app._open_skills_dialog()

    def open_tools_dialog(self) -> None:
        self._app._open_tools_dialog()

    async def persist_default_model_choice(self, model: str) -> None:
        await self._app._persist_default_model_choice(model)

    # ------------------------------------------------------------------
    # External managers
    # ------------------------------------------------------------------

    def screen_router_open_sessions(self) -> None:
        self._app._screen_router.open_sessions()

    def screen_router_open_workspaces_screen(self) -> None:
        self._app._screen_router.open_workspaces_screen()

    def screen_router_open_projects_screen(self) -> None:
        self._app._screen_router.open_projects_screen()

    def screen_router_open_platform_screen(self, name: str) -> None:
        # ``open_platform_screen`` is async because it has to defer the
        # default-project lookup off the TUI loop. Schedule it through the
        # app's command worker so the slash dispatch returns immediately.
        self._app._run_command(self._app._screen_router.open_platform_screen, name)

    def screen_router_open_console(self) -> None:
        self._app._screen_router.open_console()

    def screen_router_open_report_bug(self) -> None:
        self._app._screen_router.open_report_bug()

    def screen_router_open_raw_spans_screen(self) -> None:
        self._app._screen_router.open_raw_spans_screen()

    def screen_router_open_capabilities_screen(self) -> None:
        self._app._screen_router.open_capabilities_screen()

    def screen_router_open_services_screen(self) -> None:
        self._app._screen_router.open_services_screen()

    def screen_router_open_theme_showcase(self) -> None:
        self._app._screen_router.open_theme_showcase()

    def model_manager_open_model_browser_screen(self) -> None:
        self._app._model_manager.open_model_browser_screen()

    def profile_manager_login_command(self, args: list[str]) -> t.Awaitable[None]:
        return self._app._profile_manager.login_command(args)

    def profile_manager_logout_command(self) -> t.Awaitable[None]:
        return self._app._profile_manager.logout_command()

    def profile_manager_switch_profile(self, args: list[str]) -> t.Awaitable[None]:
        # ``switch_profile`` takes a single profile name, not a list.
        return self._app._profile_manager.switch_profile(args[0] if args else "")

    def profile_manager_open_profile_dialog(self) -> None:
        self._app._profile_manager.open_profile_dialog()

    def profile_manager_apply_auth_profile(self, profile: Profile) -> t.Awaitable[bool]:
        return self._app._profile_manager.apply_auth_profile(profile)

    def exit_app(self) -> None:
        self._app.exit()

    # ------------------------------------------------------------------
    # Profile / platform / package bridges
    # ------------------------------------------------------------------
    #
    # Each of these resolves a bare name inside ``app.py`` at call time,
    # so tests that do ``monkeypatch.setattr("dreadnode.app.tui.app.X", ...)``
    # intercept the call coming from the dispatcher. If these were plain
    # imports in ``command_dispatcher.py``, the patches would be shadowed
    # by the dispatcher's own module-scoped binding.

    def active_profile(self) -> tuple[str | None, Profile | None]:
        return _active_profile()

    def platform_client(self) -> tuple[t.Any, Profile]:
        return _platform_client()

    def save_profile(self, name: str, profile: Profile) -> Profile:
        return _save_profile(name, profile)

    def parse_pull_ref(self, raw: str, *, default_org: str) -> tuple[str, t.Any]:
        return _parse_tui_pull_ref(raw, default_org=default_org)

    def package_pull(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        return Package.pull(*args, **kwargs)

    def make_storage(self, *, profile: Profile, api: t.Any) -> t.Any:
        return Storage(profile=profile, api=api)


# ─────────────────────────────────────────────────────────────────────────────
# CapabilitiesManager adapter
# ─────────────────────────────────────────────────────────────────────────────
#
# Narrow surface the :class:`CapabilitiesManager` uses to push state back
# into the app. Everything else (tests, other managers) continues to read
# ``self.runtime_info`` on the app — which is a property that delegates
# to the manager — so the refactor is a drop-in replacement for the
# previous grab-bag of helper methods.


# ─────────────────────────────────────────────────────────────────────────────
# TurnCoordinator adapter
# ─────────────────────────────────────────────────────────────────────────────
#
# Single fat adapter implementing :class:`TurnCoordinatorActions`.
# The coordinator drives a whole turn end-to-end (stream, event
# dispatch, auth error, cleanup, queue drain) — everything it needs
# routes through this one adapter, analogous to the other manager
# adapters above.


@dataclass(slots=True)
class _AppTurnActions:
    _app: "DreadnodeTextualApp"

    # ------------------------------------------------------------------
    # Server transport
    # ------------------------------------------------------------------

    def stream_chat(
        self,
        *,
        session_id: str,
        message: str,
        model: str,
        agent: str | None,
        generate_params_extra: dict[str, t.Any] | None,
    ) -> t.AsyncIterator[dict[str, t.Any]]:
        return self._app.managed_client.stream_chat(
            session_id=session_id,
            message=message,
            model=model,
            agent=agent,
            generate_params_extra=generate_params_extra,
        )

    async def execute_shell(self, command: str) -> dict[str, t.Any]:
        return await self._app.managed_client.execute_shell(command)

    async def cancel_session(self, session_id: str) -> None:
        await self._app.managed_client.cancel_session(session_id)

    async def send_permission_response(
        self, session_id: str, request_id: str, decision: str
    ) -> None:
        await self._app.managed_client.send_permission_response(session_id, request_id, decision)

    async def send_human_input_response(
        self, session_id: str, response: HumanInputResponse
    ) -> None:
        await self._app.managed_client.send_human_input_response(session_id, response)

    # ------------------------------------------------------------------
    # App state
    # ------------------------------------------------------------------

    def active_session(self) -> SessionRecord | None:
        return self._app._active_session()

    def active_session_id(self) -> str | None:
        return self._app.active_session_id

    def current_model(self) -> str:
        return self._app.model

    def generate_params_extra(self) -> dict[str, t.Any]:
        return self._app.generate_params_extra

    def is_authenticated(self) -> bool:
        return self._app.authenticated

    # ------------------------------------------------------------------
    # Session manager side effects
    # ------------------------------------------------------------------

    def handle_event(self, event: dict[str, t.Any], session_id: str) -> None:
        self._app._handle_event(event, session_id)

    def commit_draft_to_transcript(self, session_id: str) -> None:
        self._app._sessions_manager.commit_draft_to_transcript(session_id)

    def session_turn_state(self, session_id: str) -> t.Any:
        return self._app._sessions_manager.session_turn_state(session_id)

    def notify_agent_output_available(self, session_id: str) -> None:
        self._app._write_agent_output_pointer(session_id)

    def abort_running_tools(self, session_id: str) -> None:
        self._app._sessions_manager.abort_running_tools(session_id)

    def apply_human_prompt_response(self, session_id: str, action: str) -> None:
        self._app._sessions_manager.apply_human_prompt_response(session_id, action)

    def active_human_prompt(self) -> HumanPrompt | None:
        return self._app._sessions_manager.active_human_prompt()

    def display_agent_for(self, session_info: SessionInfo) -> str:
        return self._app._capabilities_manager.session_display_agent(session_info)

    def sync_queue(self) -> None:
        self._app._sessions_manager.sync_queue()

    def sync_sessions(self) -> None:
        self._app._sync_sessions()

    def schedule_runtime_session_subscription_sync(self) -> None:
        self._app._schedule_runtime_session_subscription_sync()

    # ------------------------------------------------------------------
    # Model manager
    # ------------------------------------------------------------------

    async def ensure_litellm_key_fresh(self) -> None:
        await self._app._model_manager.ensure_litellm_key_fresh()

    # ------------------------------------------------------------------
    # Auth handler
    # ------------------------------------------------------------------

    def handle_authentication_error(self, message: str) -> None:
        self._app._profile_manager.handle_authentication_error(message)

    # ------------------------------------------------------------------
    # Turn lifecycle — direct access
    # ------------------------------------------------------------------

    def turn_lifecycle(self) -> TurnLifecycle:
        return self._app._turn

    # ------------------------------------------------------------------
    # UI widgets
    # ------------------------------------------------------------------

    def query_tool_progress(self) -> ToolProgress:
        return self._app.query_one("#tool-progress", ToolProgress)

    def query_composer(self) -> ComposerInput:
        return self._app.query_one("#composer", ComposerInput)

    def query_permission_prompt(self) -> HumanPromptWidget:
        return self._app.query_one("#human-prompt", HumanPromptWidget)

    def append_transcript(
        self,
        message: Message,
        session_id: str,
        **kwargs: t.Any,
    ) -> None:
        # ``**kwargs`` so tests which assert ``assert_any_call(msg, sid)``
        # without the ``scroll`` kwarg still see a matching call — the
        # default is passed through only when the coordinator explicitly
        # sets it, matching the old direct-call shape.
        self._app._append_transcript(message, session_id, **kwargs)

    def write_activity(self, message: str, *, style: str = "info") -> None:
        self._app._write_activity(message, style=style)

    def flash(self, message: str, *, severity: str = "info") -> None:
        self._app._flash(message, severity=severity)

    # ------------------------------------------------------------------
    # Session creation hook
    # ------------------------------------------------------------------

    async def ensure_active_session(self) -> SessionRecord | None:
        if self._app._active_session() is None:
            await self._app._create_new_session_impl()
        return self._app._active_session()

    # ------------------------------------------------------------------
    # Worker scheduling — re-enter the app's ``@work`` wrappers
    # ------------------------------------------------------------------

    def schedule_send_chat(self, message: str, *, agent: str | None = None) -> None:
        if agent is None:
            self._app._send_chat(message)
        else:
            self._app._send_chat_to_agent(message, agent)

    def schedule_send_human_input_response(
        self,
        request_id: str,
        action: t.Literal["submit", "cancel"],
        *,
        answers: list[QuestionAnswer] | None = None,
    ) -> None:
        self._app._send_human_input_response(
            request_id,
            action,
            answers=answers,
        )

    def cancel_session_workers(self) -> None:
        self._app.workers.cancel_group(self._app, "session")

    def cancel_server_turn(self) -> None:
        # Delegates at call time so tests that patch
        # ``app._cancel_server_turn = MagicMock()`` still intercept the
        # cancel path from inside the coordinator's interrupt sequence.
        self._app._cancel_server_turn()

    # ------------------------------------------------------------------
    # Session count bookkeeping
    # ------------------------------------------------------------------

    def session_transcript_length(self, session_id: str) -> int:
        record = self._app.sessions.get(session_id)
        return len(record.transcript) if record is not None else 0

    def set_session_message_count(self, session_id: str, count: int) -> None:
        record = self._app.sessions.get(session_id)
        if record is not None:
            record.info.message_count = count


@dataclass(slots=True)
class _AppCapabilitiesContext:
    _app: "DreadnodeTextualApp"

    def managed_client(self) -> ManagedRuntimeClient:
        return self._app.managed_client

    def set_working_dir(self, working_dir: str) -> None:
        self._app.working_dir = working_dir

    def set_mention_agents(self, agents: list[dict[str, str]]) -> None:
        self._app.query_one("#mention-overlay", MentionOverlay).set_agents(agents)

    def set_runtime_health(self, groups: tuple[tuple[str, str, str, str], ...]) -> None:
        self._app.runtime_health = groups

    def sync_sessions(self) -> None:
        self._app._sync_sessions()

    def update_context(self) -> None:
        self._app._update_context()

    async def refresh_skill_names(self) -> None:
        await self._app._command_dispatcher.refresh_skill_names()

    def open_capabilities_screen(self) -> None:
        self._app._screen_router.open_capabilities_screen()

    def set_welcome_capabilities(self, summary: CapabilitiesSummary | None) -> None:
        # Welcome stays in DOM after dismiss (hidden via CSS class), so the
        # query is safe even when the user has already started a session and
        # later opens Ctrl+P, installs a capability, and returns without
        # sending — the welcome's snapshot updates underneath.
        with contextlib.suppress(Exception):
            self._app.query_one("#welcome", Welcome).capabilities_summary = summary


class DreadnodeTextualApp(App[None]):
    """Server-first Textual frontend for the Dreadnode runtime."""

    CSS_PATH = "dreadnode.tcss"
    ENABLE_COMMAND_PALETTE = False

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("ctrl+b", "open_sessions", "Sessions", show=False),
        Binding("ctrl+w", "open_workspaces", "Workspaces", show=False),
        Binding("ctrl+o", "toggle_output_mode", "Output", show=False),
        Binding("ctrl+p", "open_capabilities", "Caps", show=False),
        Binding("ctrl+r", "open_runtimes", "Runs", show=False),
        Binding("ctrl+t", "open_traces", "Traces", show=False),
        Binding("ctrl+e", "open_evaluations", "Evals", show=False),
        Binding("f5", "open_console", "Console", show=False),
        Binding("ctrl+a", "select_agent", "Agent", show=False),
        Binding("ctrl+k", "select_model", "Model", show=False),
        Binding("ctrl+shift+k", "cycle_effort", "Effort", show=False),
        Binding("ctrl+n", "new_session", "New", show=False),
        Binding("ctrl+q", "quit", "Quit", show=False, priority=True),
        Binding("tab", "cycle_focus", "Focus", show=False),
        Binding("escape", "handle_escape", "Escape", show=False),
    ]

    # -- Reactives bound to widgets via data_bind --
    status_text: reactive[str] = reactive(STATUS_READY)
    boot_status: reactive[str] = reactive(STATUS_STARTING)
    session_label: reactive[str] = reactive("none")
    busy: reactive[bool] = reactive(False)
    connection_status: reactive[str] = reactive("")
    authenticated: reactive[bool] = reactive(False)
    agent_name: reactive[str] = reactive("default")
    working_dir: reactive[str] = reactive("")
    connection: reactive[str] = reactive("local")
    runtime_connected: reactive[bool] = reactive(False)
    last_input_tokens: reactive[int] = reactive(0)
    model_max_tokens: reactive[int] = reactive(0)
    tool_call_count: reactive[int] = reactive(0)
    cost_usd: reactive[float] = reactive(0.0)
    cost_unknown: reactive[bool] = reactive(False)
    subagent_cost_usd: reactive[float] = reactive(0.0)
    workspace_label: reactive[str] = reactive("")
    model_name: reactive[str] = reactive("")
    effort_label: reactive[str] = reactive("")
    background_status: reactive[str] = reactive("")
    runtime_health: reactive[tuple[tuple[str, str, str, str], ...]] = reactive(())
    update_available: reactive[str] = reactive("")
    remote_info: reactive[str] = reactive("")
    output_mode: reactive[str] = reactive("compact")

    def watch_model_name(self, value: str) -> None:
        """Update model_max_tokens when the active model changes."""
        from dreadnode.app.tui.model_variants import get_model_max_input_tokens

        self.model_max_tokens = get_model_max_input_tokens(value) or 0

    def __init__(
        self,
        server_url: str | None = None,
        profile: Profile | None = None,
        platform_url: str | None = None,
        resume_session_id: str | None = None,
        initial_model: str | None = None,
        initial_agent: str | None = None,
        initial_prompt: str | None = None,
        capabilities_dirs: list[str] | None = None,
        capabilities: list[str] | None = None,
        capability_flags: list[str] | None = None,
        system_prompt: str | None = None,
        initial_policy: dict[str, t.Any] | None = None,
        project_memory_preload_limit: int = 20,
    ) -> None:
        super().__init__()
        self.server_url = server_url

        # Resolve profile: explicit Profile object > platform_url string > None
        if profile is None and platform_url:
            config = UserConfig.read()
            match = config.find_by_url(platform_url)
            profile = match[1] if match else Profile(url=platform_url)

        self._current_profile = profile
        self._resume_session_id = resume_session_id
        self._initial_agent = initial_agent
        self._initial_prompt = initial_prompt
        self._initial_policy = initial_policy
        self._project_memory_preload_limit = project_memory_preload_limit
        self._scope_state: dict[str, tuple[t.Any, str | None]] = {}
        self._guard_config: dict[str, dict[str, t.Any]] = {}
        self.model: str = initial_model or self._model_from_profile(profile)
        self._model_explicitly_set: bool = initial_model is not None
        from dreadnode.app.tui.connection import RuntimeConnectionManager

        self._connection_manager = RuntimeConnectionManager(
            local_client=ManagedRuntimeClient(
                server_url=server_url,
                auto_start=server_url is None,
                capability_dirs=capabilities_dirs,
                enabled_capabilities=capabilities,
                capability_flag_overrides=capability_flags,
                system_prompt_append=system_prompt,
            ),
            on_stash_state=lambda: self._sessions_manager.stash_state(),
            on_restore_state=self._restore_session_state,
            on_after_connect=self._on_remote_connected,
            on_after_disconnect=self._on_remote_disconnected,
        )
        self._capabilities_manager = CapabilitiesManager(
            context=_AppCapabilitiesContext(self),
        )
        self.active_session_id: str | None = None
        # Apply sane default thinking effort for the initial model
        from dreadnode.app.tui.model_variants import default_effort

        _initial_effort = default_effort(self.model)
        self.thinking_enabled: bool = _initial_effort is not None
        # Per-model variant state: model_id → effort label (e.g. "high")
        # Empty string means user explicitly disabled thinking for that model.
        self._model_variants: dict[str, str] = {}
        if _initial_effort:
            self._model_variants[self.model] = _initial_effort
            self.effort_label = _initial_effort
        self._show_thinking: bool = True  # Expanded by default

        # Prompt history
        self._prompt_history: list[str] = []
        self._history_index: int = -1
        self._history_stash: str = ""

        # Turn lifecycle — single owner of busy state and generation counter.
        self._turn = TurnLifecycle(
            set_status=lambda text, busy: self._set_status(text, busy=busy),
            set_composer_enabled=lambda enabled: self._set_composer_enabled(enabled),
            focus_composer=lambda: self.query_one("#composer", ComposerInput).focus(),
        )

        # Platform model + LiteLLM proxy state
        self._model_catalog_state = ModelCatalogState()
        self._profile_flow_state = ProfileFlowState()
        self._model_manager = ModelManager(
            state=self._model_catalog_state,
            context=_AppModelCatalogContext(self),
            ui_host=_AppModelUiHost(self),
            runner=_AppModelRunner(self),
            notifier=_AppModelNotifier(self),
            actions=_AppModelSelectionActions(self),
        )
        self._profile_manager = ProfileManager(
            flow_state=self._profile_flow_state,
            state=_AppProfileState(self),
            ui=_AppProfileUi(self),
            screen=_AppProfileScreen(self),
            runtime=_AppProfileRuntime(self),
            models=_AppProfileModels(self),
            store=_AppProfileStore(),
            async_actions=_AppProfileAsyncActions(self),
        )
        self._screen_router = ScreenRouter(
            host=_AppScreenHost(self),
            sessions=_AppSessionView(self),
            runtime=_AppRuntimeView(self),
            actions=_AppScreenRouterActions(self),
        )
        self._error_handler = ErrorHandler(
            model_view=_AppProxyModelView(self),
            warnings=_AppWarningSink(self),
            proxy_auth=_AppProxyAuthActions(self),
        )
        self._sessions_manager = SessionsManager(
            ui=_AppSessionsUi(self),
            context=_AppSessionsContext(self),
            transport=_AppSessionsTransport(self),
            error_handler=self._error_handler,
            model_access=_AppSessionsModelAccess(self),
        )
        self._command_dispatcher = CommandDispatcher(
            actions=_AppCommandActions(self),
        )
        self._turn_coordinator = TurnCoordinator(
            actions=_AppTurnActions(self),
        )

        # Double-tap tracking for quit (shared by Escape and Ctrl+Q)
        self._last_quit_time: float = 0.0

        # Staged double-esc tracking for the /rewind picker (ENG-6776).
        # First Escape with text in the composer clears it and arms the
        # gesture; a second Escape inside the window opens the picker.
        # An Escape on an empty idle composer also opens the picker via
        # the explicit branch in ``action_handle_escape``.
        self._rewind_arm_time: float = 0.0
        self._rewind_arm_window: float = 0.6

        # Update check state
        self._update_check_done: bool = False

        # Skill names for slash overlay and command dispatch: set of (name, description)
        self._skill_names: set[tuple[str, str]] = set()

        # Load persistent prompt history
        self._load_prompt_history()

        # Sync model name to status bar
        self.model_name = self.model

        # Make unrecognised syntax tokens (Token.Error) render as plain text
        # instead of alarming red — Pygments often misclassifies unlabelled blocks.
        from pygments.token import Token
        from textual.highlight import HighlightTheme

        HighlightTheme.STYLES[Token.Error] = "$text 80%"

        self.register_theme(
            Theme(
                name="dreadnode",
                primary=BRAND,
                secondary=SUCCESS,
                accent=INFO,
                warning=WARNING,
                error=ERROR,
                success=SUCCESS,
                dark=True,
                background=BG,
                surface=BG,
                panel=BG,
                variables={
                    # Calm markdown headers — avoid primary orange bleeding in.
                    # H1-H4 share $fg so headings read against $fg-subtle body
                    # copy; H5/H6 step down to $fg-muted.
                    "markdown-h1-color": FG,
                    "markdown-h1-text-style": "bold",
                    "markdown-h2-color": FG,
                    "markdown-h2-text-style": "bold",
                    "markdown-h3-color": FG,
                    "markdown-h3-text-style": "bold",
                    "markdown-h4-color": FG,
                    "markdown-h4-text-style": "bold",
                    "markdown-h5-color": FG_SUBTLE,
                    "markdown-h5-text-style": "bold",
                    "markdown-h6-color": FG_MUTED,
                    "markdown-h6-text-style": "bold",
                },
            )
        )
        self.theme = "dreadnode"

    @property
    def managed_client(self) -> ManagedRuntimeClient:
        """Active runtime client — follows local/remote switching."""
        return self._connection_manager.active_client

    @property
    def sessions(self) -> dict[str, SessionRecord]:
        """Live sessions dict, owned by :class:`SessionsManager`."""
        return self._sessions_manager.sessions

    @sessions.setter
    def sessions(self, value: dict[str, SessionRecord]) -> None:
        self._sessions_manager.replace_sessions(value)

    @property
    def runtime_info(self) -> RuntimeInfo | None:
        """Latest capability snapshot, owned by :class:`CapabilitiesManager`."""
        return self._capabilities_manager.runtime_info

    @runtime_info.setter
    def runtime_info(self, value: RuntimeInfo | None) -> None:
        self._capabilities_manager.runtime_info = value

    @property
    def _pending_capability_reload(self) -> bool:
        """Pending runtime-reload flag, owned by :class:`CapabilitiesManager`."""
        return self._capabilities_manager.pending_capability_reload

    @_pending_capability_reload.setter
    def _pending_capability_reload(self, value: bool) -> None:
        self._capabilities_manager.pending_capability_reload = value

    @property
    def _pending_fix_message(self) -> str | None:
        """Pending capabilities-fix message, owned by :class:`CapabilitiesManager`."""
        return self._capabilities_manager.pending_fix_message

    @_pending_fix_message.setter
    def _pending_fix_message(self, value: str | None) -> None:
        self._capabilities_manager.pending_fix_message = value

    @property
    def _tool_call_widgets(self) -> dict[str, t.Any]:
        """In-flight ToolCall widgets keyed by tool_call_id, owned by SessionsManager."""
        return self._sessions_manager.tool_call_widgets

    @property
    def _last_auth_error(self) -> dict[str, str]:
        """Most recent authentication error text per session, owned by SessionsManager."""
        return self._sessions_manager.last_auth_error

    @property
    def generate_params_extra(self) -> dict[str, t.Any]:
        """Build generate_params_extra from current thinking/effort settings."""
        if not self.thinking_enabled or not self.effort_label:
            return {}
        from dreadnode.app.tui.model_variants import get_variants

        variants = get_variants(self.model)
        if self.effort_label in variants:
            return dict(variants[self.effort_label])
        return {}

    # ==================================================================
    # Compose
    # ==================================================================

    def compose(self) -> ComposeResult:
        with Vertical(id="main-body"):
            yield self._build_welcome()
            yield ConversationView(
                id="conversation",
            )
            yield NewMessagesPill(id="new-messages-pill")
            yield ToolProgress(id="tool-progress")
            yield HumanPromptWidget(id="human-prompt")
            yield SlashOverlay(id="slash-overlay")
            yield MentionOverlay(id="mention-overlay")
            yield RewindPickerOverlay(id="rewind-picker-overlay")
            yield AgentDialog(id="agent-dialog")
            yield ProfileDialog(id="profile-dialog")
            yield SkillsDialog(id="skills-dialog")
            yield ToolsDialog(id="tools-dialog")
            yield Flash(id="flash")
            yield MessageQueue(id="message-queue")
            yield self._build_context_bar()  # Zone 1
            yield Horizontal(  # Zone 2
                Static("> ", id="prompt-char"),
                ComposerInput(id="composer"),
                id="composer-bar",
            )
            yield self._build_page_status()  # Zone 3
        yield self._build_status_bar()  # Zone 4

    def _build_welcome(self) -> Welcome:
        try:
            from dreadnode.version import VERSION
        except Exception:
            logger.opt(exception=True).debug("Could not import VERSION")
            version = ""
        else:
            version = f"v{VERSION}"
        welcome = Welcome(id="welcome")
        welcome.version = version
        welcome.working_dir = str(Path.cwd())
        welcome.data_bind(
            runtime_connected=DreadnodeTextualApp.runtime_connected,
        )
        # Seed from the manager in case runtime_info hydrated before compose
        # (e.g. fast cache hit). Stays None otherwise; the manager pushes a
        # fresh summary via the context port as soon as runtime info arrives.
        welcome.capabilities_summary = self._capabilities_manager.welcome_capabilities_summary()
        return welcome

    def _build_context_bar(self) -> ContextBar:
        bar = ContextBar(id="context-bar")
        bar.data_bind(
            agent_name=DreadnodeTextualApp.agent_name,
            session_label=DreadnodeTextualApp.session_label,
            model_name=DreadnodeTextualApp.model_name,
            effort_label=DreadnodeTextualApp.effort_label,
            busy=DreadnodeTextualApp.busy,
            status_text=DreadnodeTextualApp.status_text,
            background_status=DreadnodeTextualApp.background_status,
            output_mode=DreadnodeTextualApp.output_mode,
        )
        return bar

    def _build_page_status(self) -> PageStatus:
        status = PageStatus(id="page-status")
        status.data_bind(
            last_input_tokens=DreadnodeTextualApp.last_input_tokens,
            model_max_tokens=DreadnodeTextualApp.model_max_tokens,
            tool_call_count=DreadnodeTextualApp.tool_call_count,
            cost_usd=DreadnodeTextualApp.cost_usd,
            cost_unknown=DreadnodeTextualApp.cost_unknown,
            subagent_cost_usd=DreadnodeTextualApp.subagent_cost_usd,
            runtime_issues=DreadnodeTextualApp.runtime_health,
        )
        return status

    def _build_status_bar(self) -> StatusBar:
        bar = StatusBar(id="status-bar")
        bar.data_bind(
            connection=DreadnodeTextualApp.connection,
            runtime_connected=DreadnodeTextualApp.runtime_connected,
            connection_status=DreadnodeTextualApp.connection_status,
            boot_status=DreadnodeTextualApp.boot_status,
            workspace_label=DreadnodeTextualApp.workspace_label,
            update_available=DreadnodeTextualApp.update_available,
            remote_info=DreadnodeTextualApp.remote_info,
        )
        return bar

    # ==================================================================
    # Watchers
    # ==================================================================

    def watch_runtime_connected(self, value: bool) -> None:
        if value:
            self.connection_status = ""

    def watch_authenticated(self, value: bool) -> None:
        try:
            from textual.app import ScreenStackError
            from textual.css.query import NoMatches

            composer = self.query_one("#composer", ComposerInput)
        except (NoMatches, ScreenStackError):
            logger.debug("watch_authenticated: composer not found in DOM")
            return
        composer.disabled = not value
        try:
            composer_bar = self.query_one("#composer-bar")
            composer_bar.set_class(not value, "-disabled")
        except (NoMatches, ScreenStackError):
            logger.opt(exception=True).debug("Composer bar update failed")
        if value:
            composer.focus()

    # ==================================================================
    # Lifecycle
    # ==================================================================

    def on_mount(self) -> None:
        enable_tui_capture()
        install_stdlib_intercept()
        self._set_composer_enabled(False)
        # Hide conversation while welcome is showing
        self.query_one("#conversation", ConversationView).display = False
        self._sync_conversation()
        self._sync_sessions()
        self._update_context()
        self._install_notify_subscriber(self._connection_manager.local_client)
        self._profile_manager.schedule_boot()
        self._check_for_update()

    async def on_unmount(self) -> None:
        notify_workers = self.workers.cancel_group(self, "notify-subscriber")
        for worker in notify_workers:
            with contextlib.suppress(Exception):
                await asyncio.wait_for(worker.wait(), timeout=5)
        await self._connection_manager.close()

    # Tracks the focused widget across an OS focus loss so we can restore it
    # when the terminal regains focus. See on_app_blur / on_app_focus.
    _pre_blur_focus: "Widget | None" = None

    def on_app_blur(self, _event: events.AppBlur) -> None:
        """Hide input carets when the terminal loses OS focus.

        Without this, the Input/TextArea caret keeps blinking even when the
        user has switched to another window, making it look like keystrokes
        are being captured here when they aren't.
        """
        self._pre_blur_focus = self.focused
        if self.screen is not None:
            with contextlib.suppress(Exception):
                self.screen.set_focus(None)

    def on_app_focus(self, _event: events.AppFocus) -> None:
        """Restore focus to whatever was focused before the terminal blurred."""
        target = self._pre_blur_focus
        self._pre_blur_focus = None
        if target is None:
            return
        with contextlib.suppress(Exception):
            target.focus()

    # ==================================================================
    # Input handling (using @on for explicit event binding)
    # ==================================================================

    @on(TextArea.Changed, "#composer")
    def _on_composer_changed(self, event: TextArea.Changed) -> None:
        slash_overlay = self.query_one("#slash-overlay", SlashOverlay)
        mention_overlay = self.query_one("#mention-overlay", MentionOverlay)
        skills_dialog = self.query_one("#skills-dialog", SkillsDialog)
        value = event.text_area.text

        if self._sessions_manager.active_human_prompt() is not None:
            slash_overlay.hide()
            mention_overlay.hide()
            return

        # Skills browse mode: dialog is open, typing filters it
        if skills_dialog.is_visible:
            skills_dialog.filter(value)
            return

        # Slash commands: /foo
        if value.startswith("/") and " " not in value:
            mention_overlay.hide()
            skill_commands = [
                SlashCommand(f"/{name}", desc) for name, desc in sorted(self._skill_names)
            ]
            slash_overlay.filter_commands(value, extra_commands=skill_commands)
            return

        # @ mentions: show agents from capabilities
        at_match = re.search(r"@(\S*)$", value)
        if at_match:
            slash_overlay.hide()
            mention_overlay.filter(at_match.group(1))
            return

        slash_overlay.hide()
        mention_overlay.hide()

    @on(ComposerInput.Submitted)
    def _on_composer_submitted(self, event: ComposerInput.Submitted) -> None:
        value = event.value
        logger.debug(
            "Composer submitted | length={} | has_session={}",
            len(value),
            self.active_session_id is not None,
        )
        self.query_one("#slash-overlay", SlashOverlay).hide()
        self.query_one("#mention-overlay", MentionOverlay).hide()
        self._dismiss_welcome()

        if not value:
            return

        if self._sessions_manager.active_human_prompt() is not None:
            # Composer is disabled while a prompt is active — answers come
            # from the HumanPromptWidget. Drop any composer submit that
            # races past the disabled flag.
            return

        # Slash commands always execute immediately (never queued)
        if value.startswith("/"):
            self._handle_command(value)
            return

        # Shell commands always execute immediately
        if value.startswith("!"):
            shell_cmd = value[1:].strip()
            if shell_cmd:
                self._execute_shell(shell_cmd)
            return

        # Bare exit/quit commands (matches OpenCode behavior)
        if value.strip().lower() in {"exit", "quit", ":q"}:
            self.exit()
            return

        # Store in history (in-memory + persistent file)
        if value and (not self._prompt_history or self._prompt_history[-1] != value):
            self._prompt_history.append(value)
            if len(self._prompt_history) > _MAX_HISTORY:
                self._prompt_history.pop(0)
            self._save_prompt_entry(value)
        self._history_index = -1

        # If busy, queue the message instead of sending
        if self._turn.is_busy:
            self._sessions_manager.enqueue_message(value)
            return

        if at_match := re.match(r"^@(\S+)\s+([\s\S]+)$", value):
            self._send_chat_to_agent(at_match.group(2), at_match.group(1))
        else:
            # Show user message + thinking indicator immediately (before @work schedules)
            # so the first render frame already shows the conversation with user input.
            # For new sessions (no active session yet), we still show thinking state
            # immediately so the UI feels responsive during session creation.
            session = self._active_session()
            conv = self.query_one("#conversation", ConversationView)
            if session is not None:
                sid = session.info.session_id
                session.turn_count += 1
                entry = Message(
                    role="user",
                    content=value,
                    metadata={"turn": session.turn_count},
                )
                record = self.sessions.get(sid)
                if record is not None:
                    record.transcript.append(entry)
                conv.append_entry(entry)
            self._turn.start_turn("Thinking", owner=sid if session is not None else None)
            self.query_one("#tool-progress", ToolProgress).show_activity("thinking")
            self._send_chat(value, _user_entry_shown=session is not None)

    @on(ComposerInput.HelpRequested)
    def _on_help_requested(self) -> None:
        """Show help inline when ? is pressed in empty composer."""
        self._show_help()

    def on_key(self, event: "Key") -> None:
        """Global key routing for history and vim-style navigation."""
        # Only handle keys on the main screen where composer/conversation exist.
        # ID-based lookup goes through Textual's _nodes_by_id index (O(1));
        # the old class-based screen.query(ComposerInput) walked the entire
        # screen DOM and cost ~40ms per keystroke at ~120 conversation entries.
        screen = self.screen
        try:
            composer = screen.query_one("#composer", ComposerInput)
            conversation = screen.query_one("#conversation", ConversationView)
        except NoMatches:
            return

        # Overlay routing fallback — when the composer is disabled (e.g.
        # during profile recovery), route keys to the active overlay directly.
        if composer.disabled and self._has_active_overlay():
            overlay = composer._get_active_overlay()
            if overlay is not None:
                if event.key in ("up", "down"):
                    event.prevent_default()
                    event.stop()
                    overlay.move_highlight(-1 if event.key == "up" else 1)
                    return
                if event.key in ("tab", "enter"):
                    event.prevent_default()
                    event.stop()
                    overlay.select_highlighted()
                    return
                if event.key == "escape":
                    event.prevent_default()
                    event.stop()
                    # During recovery, don't dismiss the profile dialog
                    if not self.authenticated and isinstance(overlay, ProfileDialog):
                        self._flash("Select a profile to continue", severity="warning")
                    else:
                        overlay.hide()
                    return
                # Forward unhandled keys to the overlay for custom handling
                if overlay.on_key(event):
                    return

        # ? shows help when conversation is focused (composer handled via HelpRequested)
        if event.key == "question_mark" and conversation.has_focus:
            event.prevent_default()
            event.stop()
            self._show_help()
            return

        # Prompt history & queue retract: Up when cursor is on first line
        if event.key == "up" and composer.has_focus:
            on_first_line = not self._has_active_overlay() and composer.cursor_location[0] == 0
            if on_first_line and not composer.text and self._sessions_manager.has_queued_messages():
                event.prevent_default()
                message = self._sessions_manager.retract_last_queued()
                if message:
                    self._set_composer_text(composer, message)
                return
            if on_first_line:
                event.prevent_default()
                self._history_navigate(-1)
                return

        if event.key == "down" and composer.has_focus:
            last_row = len(composer.document.lines) - 1
            if not self._has_active_overlay() and composer.cursor_location[0] >= last_row:
                event.prevent_default()
                self._history_navigate(1)
                return

        # Vim-like navigation when conversation is focused
        if conversation.has_focus:
            if event.key == "j":
                event.prevent_default()
                conversation.scroll_down(animate=False)
                return
            if event.key == "k":
                event.prevent_default()
                conversation.scroll_up(animate=False)
                return
            if event.key == "g":
                event.prevent_default()
                conversation.scroll_home(animate=False)
                return
            if event.key == "G":
                event.prevent_default()
                conversation.scroll_end(animate=False)
                return
            if event.key == "ctrl+u":
                event.prevent_default()
                conversation.scroll_up(animate=False)
                conversation.scroll_up(animate=False)
                conversation.scroll_up(animate=False)
                return
            if event.key == "ctrl+d":
                event.prevent_default()
                conversation.scroll_down(animate=False)
                conversation.scroll_down(animate=False)
                conversation.scroll_down(animate=False)
                return
            if event.key == "y":
                event.prevent_default()
                self._copy_last_assistant()
                return

    def _focus_composer_if_interactive(self) -> None:
        """Restore composer focus when input should accept typing."""
        composer = self.query_one("#composer", ComposerInput)
        if composer.disabled:
            return
        composer.focus()

    @on(events.Click, "#conversation")
    def _on_conversation_clicked(self, _event: events.Click) -> None:
        """Clicks in the chat area should return typing focus to the composer."""
        if self._has_active_overlay():
            return
        self._focus_composer_if_interactive()

    @on(ConversationView.HiddenAppend)
    def _on_conversation_hidden_append(self, event: ConversationView.HiddenAppend) -> None:
        """New content arrived while the user was scrolled up — bump the pill."""
        try:
            pill = self.query_one("#new-messages-pill", NewMessagesPill)
        except NoMatches:
            return
        pill.bump(event.widget)

    @on(ConversationView.FollowingChanged)
    def _on_conversation_following_changed(self, event: ConversationView.FollowingChanged) -> None:
        """User scrolled: sync the streaming draft's follow flag and the pill.

        The draft uses this to decide whether to auto-scroll incoming tokens.
        Flipping to ``False`` mid-stream (user scrolled up) freezes the view
        at their reading position; flipping back to ``True`` resumes the live
        glued-to-bottom behavior.
        """
        try:
            draft = self.query_one("#draft", StreamingDraft)
        except NoMatches:
            pass
        else:
            draft.set_follow(event.following)

        if not event.following:
            return
        try:
            pill = self.query_one("#new-messages-pill", NewMessagesPill)
        except NoMatches:
            return
        pill.reset()

    @on(NewMessagesPill.Jump)
    def _on_pill_jump(self, _event: NewMessagesPill.Jump) -> None:
        """Pill clicked — scroll the conversation to the end and clear the counter."""
        try:
            conv = self.query_one("#conversation", ConversationView)
        except NoMatches:
            return
        conv.scroll_end(animate=False)

    def _has_active_overlay(self) -> bool:
        """Check if any overlay (slash/mention/model/agent/tools/profile) is currently visible."""
        slash = self.query_one("#slash-overlay", SlashOverlay)
        mention = self.query_one("#mention-overlay", MentionOverlay)
        rewind = self.query_one("#rewind-picker-overlay", RewindPickerOverlay)
        agent = self.query_one("#agent-dialog", AgentDialog)
        profile = self.query_one("#profile-dialog", ProfileDialog)
        skills = self.query_one("#skills-dialog", SkillsDialog)
        tools = self.query_one("#tools-dialog", ToolsDialog)
        return (
            slash.is_visible
            or mention.is_visible
            or rewind.is_visible
            or agent.is_visible
            or profile.is_visible
            or skills.is_visible
            or tools.is_visible
        )

    @on(SlashOverlay.SlashSelected)
    def _on_slash_selected(self, event: SlashOverlay.SlashSelected) -> None:
        composer = self.query_one("#composer", ComposerInput)
        from dreadnode.app.tui.commands import SLASH_COMMANDS

        cmd_def = next((c for c in SLASH_COMMANDS if c.name == event.command), None)
        # Builtins without a hint and all skills take no args — execute immediately
        is_skill = cmd_def is None and any(
            name == event.command.lstrip("/") for name, _ in self._skill_names
        )
        if is_skill or (cmd_def and not cmd_def.hint):
            composer.load_text("")
            self._handle_command(event.command)
            return
        text = event.command + " "
        composer.load_text(text)
        composer.move_cursor_relative(rows=0, columns=len(text))
        composer.focus()

    @on(MentionOverlay.AgentSelected)
    def _on_agent_mentioned(self, event: MentionOverlay.AgentSelected) -> None:
        composer = self.query_one("#composer", ComposerInput)
        # Replace the @prefix at the end with the selected agent name
        current = composer.value
        at_match = re.search(r"@\S*$", current)
        if at_match:
            before = current[: at_match.start()]
            text = f"{before}@{event.agent_name} "
        else:
            text = f"{current}@{event.agent_name} "
        composer.load_text(text)
        composer.move_cursor_relative(rows=0, columns=len(text))
        composer.focus()

    @on(HumanPromptWidget.Submit)
    def _on_human_prompt_submit(self, event: HumanPromptWidget.Submit) -> None:
        self._reset_composer_after_prompt()
        self._send_human_input_response(
            event.request_id,
            "submit",
            answers=event.answers,
        )

    @on(HumanPromptWidget.Cancel)
    def _on_human_prompt_cancel(self, event: HumanPromptWidget.Cancel) -> None:
        self._reset_composer_after_prompt()
        self._send_human_input_response(event.request_id, "cancel")

    def _reset_composer_after_prompt(self) -> None:
        """Restore composer state once an ``ask_user`` prompt resolves."""
        try:
            composer = self.query_one("#composer", ComposerInput)
        except Exception:
            return
        composer.placeholder = ""
        composer.disabled = False

    # ==================================================================
    # Actions (keybindings)
    # ==================================================================

    def action_open_sessions(self) -> None:
        self._screen_router.open_sessions()

    def _on_session_picked(self, result: str | None) -> None:
        """Handle the session picker's dismissal result.

        Lifecycle actions (archive / freeze / delete) execute inside the
        picker against the runtime — there's no defer-and-apply protocol
        on this callback anymore. The picker's contract is now purely
        "what did the user pick": ``None`` (Escape), ``"__new__"`` (new
        session), or a ``session_id`` to switch to.

        After any in-picker delete, the active session may have been
        removed from ``self.sessions``; ``_sync_after_picker_actions``
        catches that and lands the user on a sensible neighbor.
        """
        self._apply_session_picker_result(result)

    # NOTE: session-management workers (picker-result / switch / create / reset)
    # live in their own ``"session-switch"`` group so they do **not** preempt
    # the in-flight chat worker. If they shared the chat's group, opening the
    # sessions picker would cancel a paused ``ask_user`` prompt. Chat-side
    # workers stay in ``"session"`` so two chats can't run concurrently.
    @work(exclusive=True, group="session-switch")
    async def _apply_session_picker_result(self, action: str | None) -> None:
        """Process the selected action returned by the session picker."""
        if action == "__new__":
            self._dismiss_welcome()
            await self._create_new_session_inner(self._selected_agent_for_new_session())
            return

        if action and action in self.sessions:
            # Inline the switch logic — cannot call _switch_session here
            # because it's @work(exclusive=True, group="session-switch") and
            # would preempt this worker (same group).
            session_id = action
            self._dismiss_welcome()
            self.active_session_id = session_id
            self._sessions_manager.clear_session_unread(session_id)
            restored_model = self.sessions[session_id].model
            if restored_model != self.model:
                self._on_model_changed(restored_model)
            self.last_input_tokens = 0
            self.tool_call_count = 0
            self.cost_usd = 0.0
            self.cost_unknown = False
            self.subagent_cost_usd = 0.0
            await self._sessions_manager.load_transcript(session_id)
            self._sync_active_session_projection()
            self._sync_sessions()
            self._sessions_manager.sync_queue()
            self._update_context()
            return

        # Escape (or no selection). If the active session was deleted from
        # inside the picker, land the user on a neighbor — being dumped
        # back on the conversation pane for a now-gone session would be
        # confusing. When no sessions remain we surface the welcome screen
        # instead of silently materializing a new ``Session <timestamp>``.
        if self.active_session_id is not None and self.active_session_id not in self.sessions:
            self.active_session_id = next(iter(self.sessions), None) if self.sessions else None
            if self.active_session_id is None:
                self._sync_conversation()
                self._sync_active_session_projection()
                self._sync_sessions()
                self._update_context()
                self._show_welcome()
                return
            restored_model = self.sessions[self.active_session_id].model
            if restored_model != self.model:
                self._on_model_changed(restored_model)
            self._sync_conversation()
            self._sync_active_session_projection()
            self._sessions_manager.sync_queue()
            self._update_context()

    def action_new_session(self) -> None:
        self._create_new_session(self._selected_agent_for_new_session())

    def action_select_model(self) -> None:
        """Toggle the full-screen model browser (same surface as /models)."""
        self._model_manager.open_model_browser_screen()

    def action_select_agent(self) -> None:
        """Toggle agent picker dialog."""
        dialog = self.query_one("#agent-dialog", AgentDialog)
        if dialog.is_visible:
            dialog.hide()
            return
        if not self.runtime_info:
            self._flash("No runtime info available", severity="warning")
            return
        dialog.show_agents(self._capabilities_manager.collect_agents(), current=self.agent_name)

    @on(AgentDialog.AgentSelected)
    def _on_agent_dialog_selected(self, event: AgentDialog.AgentSelected) -> None:
        if event.agent_name != self.agent_name:
            if self._active_session() is not None and self.runtime_info is not None:
                available = {agent["name"] for agent in self._capabilities_manager.collect_agents()}
                if event.agent_name == "default" or event.agent_name in available:
                    self._set_active_session_agent(event.agent_name)
            self._start_agent_session(event.agent_name)
            self._flash(f"Agent: {event.agent_name}", severity="info")

    @on(ProfileDialog.ProfileSelected)
    def _on_profile_selected(self, event: ProfileDialog.ProfileSelected) -> None:
        name, _profile = _active_profile()
        # During recovery, allow re-selecting the current profile to reconnect.
        if event.profile_name == name and self.authenticated:
            return
        self._run_command(self._profile_manager.switch_profile, event.profile_name)

    @on(ProfileDialog.ProfileDeleted)
    def _on_profile_deleted(self, event: ProfileDialog.ProfileDeleted) -> None:
        self._profile_manager.handle_profile_deleted(event.profile_name)

    def action_cycle_effort(self) -> None:
        """Cycle through thinking effort levels for the current model."""
        from dreadnode.app.tui.model_variants import cycle_variant, get_variants

        variants = get_variants(self.model)
        if not variants:
            return  # Silent no-op for unsupported models

        current = self.effort_label if self.thinking_enabled else None
        next_label = cycle_variant(variants, current)

        if next_label is None:
            # Cycling past max → disable (store "" to preserve user choice)
            self.thinking_enabled = False
            self._model_variants[self.model] = ""
            self.effort_label = ""
            self._flash("Thinking disabled", severity="info")
        else:
            self.thinking_enabled = True
            self._model_variants[self.model] = next_label
            self.effort_label = next_label
            self._flash(f"Thinking: {next_label}", severity="info")

    def _is_screen_open(self, screen_type: type) -> bool:
        """Check if a screen of the given type is anywhere in the stack."""
        return any(isinstance(s, screen_type) for s in self.screen_stack)

    def _dismiss_pushed_screens(self) -> None:
        """Pop all pushed screens so we return to the base screen before opening a new one."""
        while len(self.screen_stack) > 1:
            self.pop_screen()

    def action_open_console(self) -> None:
        self._screen_router.open_console()

    def action_report_bug(self, origin: str = "conversation") -> None:
        self._screen_router.open_report_bug(origin=origin)

    def action_open_traces(self) -> None:
        if not self._require_authenticated():
            return
        self._run_command(self._screen_router.open_platform_screen, "traces")

    def action_open_evaluations(self) -> None:
        if not self._require_authenticated():
            return
        self._run_command(self._screen_router.open_platform_screen, "evaluations")

    def action_open_runtimes(self) -> None:
        if not self._require_authenticated():
            return
        self._run_command(self._screen_router.open_platform_screen, "runtimes")

    def action_open_capabilities(self) -> None:
        self._screen_router.open_capabilities_screen()

    def open_capability_detail(self, capability: str) -> None:
        """Open the capabilities manager focused on a specific capability.

        Lets the services screen jump from an MCP server / worker detail to
        the capability that installed and runs it. Dismissing the services
        screen and pushing the capabilities screen is handled by the router.
        """
        self._screen_router.open_capabilities_screen(initial_capability=capability)

    def action_open_workspaces(self) -> None:
        if not self._require_authenticated():
            return
        self._screen_router.open_workspaces_screen()

    def action_run_update(self) -> None:
        """Trigger /update via f9 keybinding."""
        self._run_command(self._update_command)

    def action_cycle_focus(self) -> None:
        """Cycle focus between composer and conversation."""
        composer = self.query_one("#composer", ComposerInput)
        conversation = self.query_one("#conversation", ConversationView)
        if composer.has_focus:
            conversation.focus()
        else:
            composer.focus()

    def _interrupt_turn(self) -> bool:
        """Cancel the active turn, draining any queued follow-up."""
        return self._turn_coordinator.interrupt()

    def _cancel_server_turn(self) -> None:
        """Fire-and-forget: tell the server to cancel the active turn.

        Lives here rather than on :class:`TurnCoordinator` so the
        asyncio task lifecycle stays in the app (where the event loop
        is owned by Textual) and tests can patch the whole method via
        ``app._cancel_server_turn = MagicMock()``.
        """
        sid = self.active_session_id
        if not sid:
            return

        async def _do_cancel() -> None:
            try:
                await self.managed_client.cancel_session(sid)
            except Exception:
                logger.debug("Server cancel request failed (session may already be idle)")

        asyncio.get_running_loop().create_task(_do_cancel())

    async def action_quit(self) -> None:
        """Ctrl+Q: interrupt if busy, then double-press to quit.

        Overrides Textual's default ``App.action_quit`` (which would exit
        immediately) so we get an interrupt-first ladder. The action name
        stays ``quit`` so Textual's reflexive-Ctrl+C hint discovers our
        binding and flashes "Press Ctrl+Q to quit the app".
        """
        now = time.monotonic()

        if self._interrupt_turn():
            self._flash("Interrupted — press again to quit", severity="warning")
            self._last_quit_time = now
            return

        # Double-press to quit
        if (now - self._last_quit_time) < 3.0:
            self.exit()
            return

        self._last_quit_time = now
        self._flash("Press Ctrl+Q again to quit", severity="warning")

    def action_handle_escape(self) -> None:
        """Escape priority: dismiss overlays → clear composer → retract queue → interrupt → quit.

        A staged double-esc gesture (ENG-6776) layers on top: clearing
        the composer arms a brief window during which a second Escape
        opens the rewind picker. Pressing Escape on an empty, idle
        composer also opens the picker — the user is asking for "the
        thing that escapes a stuck state", and we want a single discoverable
        path even when there's nothing else for Escape to do.
        """
        composer = self.query_one("#composer", ComposerInput)

        # 1. Dismiss overlays if visible
        if self._has_active_overlay():
            profile_dialog = self.query_one("#profile-dialog", ProfileDialog)
            # During recovery (unauthenticated), don't dismiss the profile
            # dialog — the user must pick a profile to proceed.
            if not self.authenticated and profile_dialog.is_visible:
                self._flash("Select a profile to continue", severity="warning")
                return
            self.query_one("#slash-overlay", SlashOverlay).hide()
            self.query_one("#mention-overlay", MentionOverlay).hide()
            self.query_one("#rewind-picker-overlay", RewindPickerOverlay).hide()
            self.query_one("#agent-dialog", AgentDialog).hide()
            profile_dialog.hide()
            self.query_one("#skills-dialog", SkillsDialog).hide()
            self.query_one("#tools-dialog", ToolsDialog).hide()
            self._rewind_arm_time = 0.0
            return

        # 2. Clear composer if non-empty — arm the rewind gesture so a
        # second Esc inside the window opens the picker.
        if composer.value:
            composer.clear_pastes()
            composer.value = ""
            self._rewind_arm_time = time.monotonic()
            return

        # 2b. Composer is empty. If the prior Esc just cleared it, this is
        # the second tap of the staged double-esc gesture — open the picker.
        if (time.monotonic() - self._rewind_arm_time) < self._rewind_arm_window:
            self._rewind_arm_time = 0.0
            self._command_dispatcher._actions.run_command(self._rewind_command)
            return

        # 3. Retract queued message back into composer for editing
        if not self._turn.is_busy and self._sessions_manager.has_queued_messages():
            message = self._sessions_manager.retract_last_queued()
            if message:
                composer.load_text(message)
                composer.move_cursor_relative(rows=9999, columns=9999)
            return

        # 4. Interrupt busy agent
        if self._interrupt_turn():
            self._flash("Interrupted", severity="warning")
            return

        # 5. Empty composer, no queue, idle — open the rewind picker as
        # the discoverable "escape from a stuck state" path. Mirrors
        # Claude Code's behavior on Escape from an empty prompt.
        if self._active_session() is not None:
            self._command_dispatcher._actions.run_command(self._rewind_command)
            return

        # 6. Nothing to do — just ensure composer has focus
        composer.focus()

    def _require_authenticated(self) -> bool:
        if not self.authenticated:
            self._flash(
                "Not authenticated — use /login to connect to the platform",
                severity="warning",
            )
            return False
        return True

    # ==================================================================
    # Boot & runtime
    # ==================================================================

    @property
    def _server_url(self) -> str:
        """The platform server URL from the resolved profile, or the default."""
        if self._current_profile and self._current_profile.url:
            return self._current_profile.url
        return DEFAULT_PLATFORM_URL

    def on_auth_modal_profile_switch_requested(self) -> None:
        """Handle profile switch from AuthModal — dismiss and open profile picker."""
        self._profile_manager.request_auth_modal_profile_switch()

    @work(exit_on_error=False)
    async def _check_for_update(self) -> None:
        """Background version check — never blocks boot."""
        try:
            from dreadnode.app.tui.update_check import check_for_update

            info = await check_for_update()
            if info:
                self.update_available = info.latest
                # Safe: Welcome stays in DOM after dismiss (hidden via CSS class, not removed)
                self.query_one("#welcome", Welcome).update_info = info
                # If auth modal is already showing, push update info into it
                self._profile_manager.try_update_auth_modal_banner(info)
        finally:
            self._update_check_done = True

    async def _refresh_server_sessions(self, *, include_platform: bool = False) -> None:
        await self._sessions_manager.refresh_from_server(include_platform=include_platform)

    @work(exclusive=True, group="session-picker-refresh")
    async def _refresh_sessions_then_open_picker(self) -> None:
        """Refresh sessions from server, then open the picker with fresh data."""
        from dreadnode.app.tui.screens.sessions import SessionPickerScreen

        if self._is_screen_open(SessionPickerScreen):
            return
        await self._sessions_manager.refresh_from_server(include_platform=True)
        self._dismiss_pushed_screens()
        self.push_screen(
            SessionPickerScreen(
                sessions=dict(self.sessions),
                active_session_id=self.active_session_id,
                managed_client=self.managed_client,
                on_session_deleted=self._handle_picker_session_deleted,
                session_web_url=self._session_web_url,
            ),
            callback=self._on_session_picked,
        )

    def _session_web_url(self, session_id: str) -> str | None:
        """Deep-link a session to the platform monitoring transcript tab."""
        return self._build_monitoring_url(session_id)

    def _build_monitoring_url(self, session_id: str, *, view: str | None = None) -> str | None:
        """Build a deep-link to the platform's ``/agents/sessions`` grid for a session.

        Returns ``None`` when no platform context is available (no auth, no
        workspace) so callers can degrade to a notify toast. ``view`` toggles
        the grid's tab — the report tool passes ``"reports"``; the picker's
        open-in-browser leaves it unset to land on the default transcript tab.
        """
        cm = self._connection_manager
        api = cm._api_client
        org = cm._org
        workspace = cm._workspace
        if api is None or not org or not workspace or not session_id:
            return None
        url = f"{api.server_root_url}/{org}/agents/sessions?workspace={workspace}&session={session_id}"
        if view:
            url += f"&view={view}"
        return url

    def _build_agent_output_url(self, project: str | None) -> str | None:
        """Build a deep-link to the platform's Agent Output page.

        Points users at where the structured output their agents emit (via the
        ``report_item`` tool — findings, assets, capability types) actually
        lands. The page filters by workspace + project, so the caller passes
        the ``project`` the session reported into (``SessionInfo.project``) —
        not whatever project happens to be selected now — so reopening an old
        session still links to the right place. Falls back to the current
        default project only when the session recorded none. Workspace is not
        stored per session, so it comes from the live connection context.

        Returns ``None`` when no platform context is available (no auth, no
        workspace) so callers degrade to no link. The route path lives only
        here, so a future nav rename is a one-line change.
        """
        cm = self._connection_manager
        api = cm._api_client
        org = cm._org
        workspace = cm._workspace
        if api is None or not org or not workspace:
            return None
        url = f"{api.server_root_url}/{org}/agents/agent-outputs?workspace={workspace}"
        profile = self._current_profile
        resolved_project = project or (profile.default_project if profile else None)
        if resolved_project:
            url += f"&project={resolved_project}"
        return url

    def _handle_picker_session_deleted(self, session_id: str) -> None:
        """Sync the app's session map after a delete inside the picker.

        The picker fires destructive actions immediately against the
        runtime (no deferred-on-exit queue), so by the time we hear
        about a delete the platform row is already gone. The remaining
        cleanup is local: drop the in-memory ``SessionRecord`` so the
        sidebar and active-session checks in ``_on_session_picked``
        observe consistent state.
        """
        self.sessions.pop(session_id, None)

    # ==================================================================
    # Session management (all async methods use @work)
    # ==================================================================

    @work(exclusive=True, group="session-switch")
    async def _create_new_session(self, agent: str | None = None) -> None:
        await self._create_new_session_inner(agent)

    def _selected_agent_for_new_session(self) -> str | None:
        """Return the selected non-default agent for an explicit new session."""
        session = self._active_session()
        agent_name = (
            self._capabilities_manager.session_display_agent(session.info)
            if session is not None
            else self.agent_name
        )
        default_agent = self._capabilities_manager.default_agent_name()
        if not agent_name or agent_name in {"default", default_agent}:
            return None
        available = {agent["name"] for agent in self._capabilities_manager.collect_agents()}
        if agent_name in available:
            return agent_name
        return None

    async def _create_new_session_impl(
        self,
        agent: str | None = None,
        *,
        policy: dict[str, t.Any] | None = None,
    ) -> None:
        """Plain-await entry point to :meth:`_create_new_session_inner`.

        Adapters like :class:`_AppProfileRuntime` need to call session
        creation from a non-``@work`` context (the boot worker already
        owns the session group). Going through ``_create_new_session``
        would schedule a second worker and return immediately; this
        wrapper just awaits the private implementation directly.
        """
        await self._create_new_session_inner(agent, policy=policy)

    async def _create_new_session_inner(
        self,
        agent: str | None = None,
        *,
        policy: dict[str, t.Any] | None = None,
    ) -> None:
        """Inner implementation -- callable from both @work and plain await."""
        self._set_status("Creating session", busy=True)
        selected_agent = None if agent == "default" else agent
        # Policy precedence: explicit arg > ``--auto`` initial policy > default.
        # Only the *first* session opened in this TUI launch inherits the CLI
        # flag; subsequent /new sessions start interactive unless the user
        # asks otherwise. Clear _initial_policy after first use so it doesn't
        # leak.
        resolved_policy = policy
        if resolved_policy is None and self._initial_policy is not None:
            resolved_policy = self._initial_policy
            self._initial_policy = None
        logger.info(
            "Session create | agent={} model={} policy={}",
            selected_agent or self._capabilities_manager.default_agent_name() or "default",
            self.model,
            resolved_policy,
        )
        session_info = await self.managed_client.create_session(
            agent=selected_agent,
            model=self.model,
            generate_params_extra=self.generate_params_extra or None,
            policy=resolved_policy,
            project_memory_preload_limit=self._project_memory_preload_limit,
        )
        # Leave ``title`` unset: the table view, sidebar, and context bar
        # render through ``SessionRecord.display_title()`` which falls back
        # to the platform-populated first-message preview (rule SES-LST-011)
        # once the user sends their first turn. ``/rename`` is the
        # canonical way to give a session a human label up front.
        self.sessions[session_info.session_id] = SessionRecord(
            info=session_info,
            model=self.model,
        )
        logger.info(
            "Session created | session={} agent={}",
            session_info.session_id[:8],
            self._capabilities_manager.session_display_agent(session_info),
        )
        self.active_session_id = session_info.session_id
        self._sessions_manager.clear_session_unread(session_info.session_id)
        await self._sync_runtime_session_subscriptions()

        self.last_input_tokens = 0
        self.tool_call_count = 0
        self.cost_usd = 0.0
        self.cost_unknown = False
        self.subagent_cost_usd = 0.0
        self._sync_conversation()
        self._sync_active_session_projection()
        self._sync_sessions()
        self._update_context()
        self._set_status("Ready", busy=False)

    async def _launch_background_task_command(self, args: list[str]) -> None:
        """Spawn an autonomous background session on a task prompt.

        Usage: ``/background <task>`` or ``/bg <task>``.

        Creates a fresh session with ``HeadlessSessionPolicy`` from
        birth and streams the task prompt into it, **without**
        changing ``active_session_id``. The user stays on whatever
        session they were viewing; the background session accrues in
        the sidebar with an ``autonomous`` policy badge and streams
        events through the normal subscription path so switching into
        it reveals a live transcript.

        Terminal events on background sessions fire a notification
        toast via the existing ``_flash`` pipeline — no new widget
        required for the first cut.
        """
        if not args:
            self._flash("/background: need a task prompt", severity="warning")
            return

        task_prompt = " ".join(args).strip()
        if not task_prompt:
            self._flash("/background: need a task prompt", severity="warning")
            return

        logger.info(
            "Launching background task | prompt={}...",
            task_prompt[:60],
        )

        try:
            session_info = await self.managed_client.create_session(
                agent=self._initial_agent or None,
                model=self.model,
                generate_params_extra=self.generate_params_extra or None,
                policy={"name": "headless", "max_steps": 30},
                project_memory_preload_limit=self._project_memory_preload_limit,
            )
        except Exception as exc:
            logger.opt(exception=True).warning("Background session create failed")
            self._flash(f"Background task failed to start: {exc}", severity="error")
            return

        sid = session_info.session_id
        # The autonomous policy is already surfaced as a status badge in the
        # picker, and the prompt itself becomes ``info.preview`` once the
        # platform persists the first user message — no need to bake either
        # into the title field.
        self.sessions[sid] = SessionRecord(
            info=session_info,
            model=self.model,
        )

        # Subscribe to the new session's event broker so the TUI
        # accumulates state even while the user is looking elsewhere.
        await self._sync_runtime_session_subscriptions()
        self._sync_sessions()

        # Kick off the turn as a detached task. We do *not* go through
        # ``_send_chat`` because that method is decorated with
        # ``@work(exclusive=True, group="session")`` — using it would
        # cancel any in-flight turn on the currently-active session.
        # Background tasks live on their own per-session asyncio tasks.
        asyncio.create_task(self._run_background_turn(sid, task_prompt))  # noqa: RUF006

        flash_preview = task_prompt[:40] + ("..." if len(task_prompt) > 40 else "")
        self._flash(
            f"Background task started: {flash_preview}",
            severity="info",
        )

    async def _run_background_turn(self, session_id: str, prompt: str) -> None:
        """Drive a single turn on a background autonomous session.

        Events flow through ``_sessions_manager.handle_event`` the
        same way as foreground turns, so the session's ``TurnState``
        populates naturally and switching to it reveals a live
        transcript. On terminal events (``AgentEnd`` / error) we
        flash a notification so the user knows the background task
        finished even if they never opened its pane.
        """
        from dreadnode.app.tui import wire_events as we
        from dreadnode.app.tui.wire_events import parse_wire_event

        session = self.sessions.get(session_id)
        if session is None:
            logger.warning("Background turn missing session | sid={}", session_id[:8])
            return

        display = session.info.session_id[:8]
        try:
            async for raw_event in self.managed_client.stream_chat(
                session_id=session_id,
                message=prompt,
                model=self.model,
                agent=None if session.info.agent == "default" else session.info.agent,
                generate_params_extra=self.generate_params_extra or None,
            ):
                self._sessions_manager.handle_event(raw_event, session_id)
                event = parse_wire_event(raw_event)
                if event is None:
                    continue
                if isinstance(event, we.AgentEnd):
                    if event.data.error:
                        self.call_from_thread(
                            self._flash,
                            f"Background task {display} failed: {event.data.error}",
                            severity="error",
                        )
                    else:
                        self.call_from_thread(
                            self._flash,
                            f"Background task {display} completed",
                            severity="info",
                        )
                    return
                if isinstance(event, we.RuntimeErrorEvent):
                    self.call_from_thread(
                        self._flash,
                        f"Background task {display} errored: {event.error}",
                        severity="error",
                    )
                    return
        except Exception as exc:
            logger.opt(exception=True).warning("Background turn crashed | sid={}", display)
            self.call_from_thread(
                self._flash,
                f"Background task {display} crashed: {exc}",
                severity="error",
            )

    async def _policy_command(self, args: list[str]) -> None:
        """Generic policy swap command: ``/policy <name> [k=v ...]``.

        With no args, flashes the public registered policy names so
        the user can discover what capabilities contributed. Experimental
        built-ins remain callable by name without being advertised. With a
        name alone, swaps to that policy with default params. With
        ``k=v`` pairs trailing, forwards them as the policy spec —
        integer-looking values are coerced to int, ``true``/``false``
        to bool, everything else stays a string.

        This is the capability-friendly path: a capability author
        ships ``policies/strict.py`` defining ``StrictPolicy`` with
        ``name="strict"``, and users run ``/policy strict
        max_steps=5``. ``/auto`` and ``/interactive`` remain as
        shortcuts for the two built-ins.
        """
        from dreadnode.policies import registered_policy_names

        if not args:
            names = [name for name in registered_policy_names() if name != "guard"]
            self._flash(f"Registered policies: {', '.join(names)}", severity="info")
            return

        if args[0] == "scope":
            await self._open_scope_modal()
            return

        session = self._active_session()
        if session is None:
            # Auto-create a session so the user doesn't have to send a
            # message first just to set a policy.
            await self._create_new_session_impl(None)
            session = self._active_session()
            if session is None:
                self._flash("Failed to create session", severity="error")
                return

        name = args[0]
        spec: dict[str, t.Any] = {"name": name}
        for kv in args[1:]:
            if "=" not in kv:
                self._flash(f"/policy: expected k=v, got {kv!r}", severity="warning")
                return
            key, raw = kv.split("=", 1)
            spec[key.strip()] = _coerce_policy_arg(raw.strip())

        # Guard policy: merge with previous config so partial changes
        # persist (e.g. changing judge_model keeps the scope, and
        # changing preset keeps the judge_model).
        if name == "guard":
            prev = self._guard_config.get(session.info.session_id, {})
            merged = {**prev, **spec}
            # If the user explicitly set a preset or scope, clear the
            # other so they don't conflict (scope takes precedence in
            # GuardSessionPolicy, which would silently ignore preset).
            if "preset" in spec:
                merged.pop("scope", None)
            if "scope" in spec:
                merged.pop("preset", None)
            if "judge_model" not in merged:
                merged["judge_model"] = "dn/claude-sonnet-4-6"
            spec = merged

        try:
            result = await self.managed_client.set_session_policy(
                session.info.session_id,
                spec,
            )
        except Exception as exc:
            logger.opt(exception=True).warning("Policy swap failed")
            self._flash(f"Policy swap failed: {exc}", severity="error")
            return

        # Store the guard config for future merges
        if name == "guard":
            self._guard_config[session.info.session_id] = spec
            # Clear stale scope modal state if preset changed via command
            if "preset" in spec and "scope" not in spec:
                self._scope_state.pop(session.info.session_id, None)

        session.info.policy_name = str(result.get("policy_name", "interactive"))
        session.info.policy_is_autonomous = bool(result.get("policy_is_autonomous", False))
        session.info.policy_display_label = str(result.get("policy_display_label", "") or "")

        # Track judge model for display in session label
        judge_model = spec.get("judge_model", "")
        if judge_model:
            session.info.policy_display_label = self._guard_display_label(str(judge_model))

        self._sync_sessions()
        self._update_context()
        self._flash(f"Policy {session.info.policy_name} updated", severity="info")

    @staticmethod
    def _guard_display_label(judge_model: str) -> str:
        """Build a short display label, e.g. ``guard · dn/claude-sonnet-4-6``."""
        return f"guard \u00b7 {judge_model}"

    async def _open_scope_modal(self) -> None:
        """Push the interactive scope policy configuration modal."""
        from dreadnode.app.tui.widgets.scope_modal import ScopePolicyModal

        session = self._active_session()
        if session is None:
            await self._create_new_session_impl(None)
            session = self._active_session()
            if session is None:
                self._flash("Failed to create session", severity="error")
                return

        saved = self._scope_state.get(session.info.session_id)
        if saved:
            caps, preset = saved
            self.push_screen(ScopePolicyModal(caps, preset), callback=self._on_scope_result)
        else:
            self.push_screen(ScopePolicyModal(), callback=self._on_scope_result)

    def _on_scope_result(self, result: dict[str, t.Any] | None) -> None:
        """Apply the scope config returned by the scope modal."""
        from dreadnode.policies.scope import ScopeCapabilities

        if result is None:
            return

        session = self._active_session()
        if session is None:
            return

        # Persist scope state locally so the modal can restore it.
        caps = ScopeCapabilities(**result.get("capabilities", {}))
        preset = result.get("preset")
        self._scope_state[session.info.session_id] = (caps, preset)

        # Merge with previous guard config to preserve judge_model
        prev = self._guard_config.get(session.info.session_id, {})
        spec: dict[str, t.Any] = {
            "name": "guard",
            "judge_model": prev.get("judge_model", "dn/claude-sonnet-4-6"),
            "scope": result,
        }
        self._guard_config[session.info.session_id] = spec

        async def _apply() -> None:
            try:
                api_result = await self.managed_client.set_session_policy(
                    session.info.session_id,
                    spec,
                )
            except Exception as exc:
                logger.opt(exception=True).warning("Scope policy swap failed")
                self._flash(f"Scope policy failed: {exc}", severity="error")
                return

            session.info.policy_name = str(api_result.get("policy_name", "interactive"))
            session.info.policy_is_autonomous = bool(api_result.get("policy_is_autonomous", False))
            session.info.policy_display_label = self._guard_display_label(spec["judge_model"])
            self._sync_sessions()
            self._update_context()
            self._flash(f"Policy {session.info.policy_name} (scope) updated", severity="info")

        self.run_worker(_apply(), exclusive=True, group="scope-policy")

    async def _set_session_policy_command(
        self,
        args: list[str],
        policy_name: str,
    ) -> None:
        """Swap the active session's policy.

        ``/auto [max_steps]`` — max_steps optional, defaults to 30.
        ``/interactive`` — no args.
        """
        session = self._active_session()
        if session is None:
            self._flash("No active session — start one first", severity="warning")
            return

        spec: str | dict[str, t.Any]
        if policy_name == "headless":
            max_steps = 30
            if args:
                try:
                    max_steps = int(args[0])
                except ValueError:
                    self._flash(
                        f"/auto: max_steps must be an integer, got {args[0]!r}",
                        severity="warning",
                    )
                    return
                if max_steps <= 0:
                    self._flash(
                        f"/auto: max_steps must be positive, got {max_steps}",
                        severity="warning",
                    )
                    return
            spec = {"name": "headless", "max_steps": max_steps}
        else:
            spec = policy_name

        try:
            result = await self.managed_client.set_session_policy(
                session.info.session_id,
                spec,
            )
        except Exception as exc:
            logger.opt(exception=True).warning("Policy swap failed")
            self._flash(f"Policy swap failed: {exc}", severity="error")
            return

        session.info.policy_name = str(result.get("policy_name", "interactive"))
        session.info.policy_is_autonomous = bool(result.get("policy_is_autonomous", False))
        session.info.policy_display_label = str(result.get("policy_display_label", "") or "")

        self._sync_sessions()
        self._update_context()
        if session.info.policy_is_autonomous:
            max_steps_label = spec["max_steps"] if isinstance(spec, dict) else "?"
            self._flash(
                f"Autonomous mode engaged — max {max_steps_label} steps",
                severity="info",
            )
        else:
            self._flash("Interactive mode restored", severity="info")

    async def _update_command(self) -> None:
        """Handle /update — check for updates and run upgrade."""
        import asyncio

        from dreadnode.app.tui.update_check import (
            build_noop_upgrade_diagnostic,
            check_for_update,
            detect_upgrade_command,
            verify_upgrade,
        )

        # If no known update, re-check PyPI (user explicitly asked)
        if not self.update_available:
            self._flash("Checking for updates...", severity="info")
            logger.info("Update check: user requested /update, checking PyPI")
            info = await check_for_update()
            if info:
                self.update_available = info.latest
                logger.info("Update check: {} -> {} available", info.current, info.latest)
            else:
                self._flash("Already up to date", severity="info")
                logger.info("Update check: already up to date")
                return

        # Dismiss welcome so the activity messages are visible
        self._dismiss_welcome()

        cmd = detect_upgrade_command()
        cmd_display = " ".join(cmd) if isinstance(cmd, list) else cmd
        logger.info("Update: running {}", cmd_display)
        self._flash("Updating Dreadnode...", severity="info")

        try:
            if isinstance(cmd, list):
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
            else:
                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
            stdout_bytes, stderr_bytes = await proc.communicate()
        except Exception as exc:
            logger.error("Update: subprocess failed: {}", exc)
            self._write_activity(f"Update failed: {exc}", style="error")
            self._flash("Update failed", severity="error")
            return

        stdout_text = stdout_bytes.decode(errors="replace").strip()
        stderr_text = stderr_bytes.decode(errors="replace").strip()

        if proc.returncode == 0:
            logger.info("Update: success (rc=0)\nstdout: {}\nstderr: {}", stdout_text, stderr_text)
            from rich.text import Text as RichText

            verified = await asyncio.to_thread(verify_upgrade, self.update_available)
            if verified:
                logger.info("Update: verified new version {}", verified)
                msg = RichText()
                msg.append("✓ ", style=f"bold {SUCCESS}")
                msg.append(f"Updated to v{verified}", style=f"bold {SUCCESS}")
                msg.append(" — restart ", style=FG_SUBTLE)
                msg.append("dn", style=f"bold {FG}")
                msg.append(" to use the new version", style=FG_SUBTLE)
                conv = self.query_one("#conversation", ConversationView)
                conv.write(RichText())  # spacer
                conv.write(msg)
                conv.write(RichText())  # spacer
                self._flash("Updated — restart dn to apply", severity="success")
                self.update_available = ""
                self.query_one("#welcome", Welcome).update_info = None
            else:
                logger.warning(
                    "Update: command succeeded but version not verified (expected {})",
                    self.update_available,
                )
                msg = RichText()
                for index, line in enumerate(
                    build_noop_upgrade_diagnostic(
                        self.update_available,
                        stdout_text,
                        stderr_text,
                    )
                ):
                    if index:
                        msg.append("\n")
                        msg.append(line, style=FG_SUBTLE)
                    else:
                        msg.append("⚠ ", style=f"bold {WARNING}")
                        msg.append(line, style=f"bold {WARNING}")
                conv = self.query_one("#conversation", ConversationView)
                conv.write(RichText())  # spacer
                conv.write(msg)
                conv.write(RichText())  # spacer
                self._flash("Update may not have applied — see details above", severity="warning")
        else:
            logger.error(
                "Update: failed (rc={})\nstdout: {}\nstderr: {}",
                proc.returncode,
                stdout_text,
                stderr_text,
            )
            error_text = stderr_text or "Unknown error"
            from rich.text import Text as RichText

            msg = RichText()
            msg.append("✗ ", style=f"bold {ERROR}")
            msg.append("Update failed\n", style=f"bold {ERROR}")
            msg.append(error_text, style=FG_MUTED)
            conv = self.query_one("#conversation", ConversationView)
            conv.write(RichText())  # spacer
            conv.write(msg)
            conv.write(RichText())  # spacer
            self._flash("Update failed — see details above", severity="error")

    async def _compact_command(self, args: list[str] | None = None) -> None:
        """Handle /compact [guidance] command."""
        session = self._active_session()
        if session is None:
            self._flash("No active session", severity="warning")
            return
        if self._turn.is_busy:
            self._flash("Cannot compact while a turn is in progress", severity="warning")
            return
        guidance = " ".join(args) if args else ""
        logger.info(
            "Session compact | session={} guidance={}", session.info.session_id[:8], bool(guidance)
        )

        my_generation = self._turn.start_turn("Compacting", owner=session.info.session_id)
        tp = self.query_one("#tool-progress", ToolProgress)
        tp.show_activity("compacting")
        owns_turn = True
        try:
            result = await self.managed_client.compact_session(
                session.info.session_id,
                guidance=guidance,
            )
        except Exception as exc:
            logger.warning(
                "Session compact failed | session={} error={}", session.info.session_id[:8], exc
            )
            self._flash(f"Compact failed: {exc}", severity="error")
            return
        finally:
            tp.hide_tool()
            owns_turn = self._turn.finish_turn(my_generation)
            if owns_turn:
                self._turn.go_idle(authenticated=self.authenticated)

        # If user interrupted (Escape) while the LLM call was in-flight,
        # finish_turn returned False — skip result processing to avoid
        # stale flashes and transcript rebuilds.
        if not owns_turn:
            logger.debug("Compact result dropped — turn was interrupted")
            return

        status = result.get("status", "failed")
        if status == "completed":
            before = result.get("messages_before", 0)
            after = result.get("messages_after", 0)
            logger.info(
                "Session compact done | session={} before={} after={}",
                session.info.session_id[:8],
                before,
                after,
            )
            # Rebuild transcript from server-side compacted messages
            await self._sessions_manager.load_transcript(session.info.session_id, force=True)
            self._sync_active_session_projection()
            self._flash(f"Compacted: {before} → {after} messages", severity="success")
        elif status == "cancelled":
            self._flash("Compaction cancelled", severity="info")
        elif status == "skipped":
            self._flash(f"Compact skipped: {result.get('reason', 'unknown')}", severity="info")
        else:
            self._flash(f"Compact failed: {result.get('reason', 'unknown')}", severity="error")

    async def _rewind_command(self) -> None:
        """Open the inline rewind picker for the active session.

        Read-only on open: candidates are pulled from the platform-side
        transcript via the runtime server, the picker shows them, and
        the actual rewind only happens once the user commits a target
        (handled by ``_on_rewind_picker_selected``).
        """
        session = self._active_session()
        if session is None:
            self._flash("No active session", severity="warning")
            return

        try:
            raw_candidates = await self.managed_client.fetch_rewind_candidates(
                session.info.session_id
            )
        except Exception as exc:
            logger.warning(
                "Rewind candidates fetch failed | session={} error={}",
                session.info.session_id[:8],
                exc,
            )
            self._flash(f"Could not load rewind targets: {exc}", severity="error")
            return

        candidates: list[RewindCandidate] = []
        for raw in raw_candidates:
            seq = raw.get("seq")
            content = raw.get("content")
            if not isinstance(seq, int) or not isinstance(content, str):
                continue
            entry: RewindCandidate = {"seq": seq, "content": content}
            created = raw.get("created_at")
            if isinstance(created, str):
                entry["created_at"] = created
            candidates.append(entry)

        picker = self.query_one("#rewind-picker-overlay", RewindPickerOverlay)
        picker.show_candidates(candidates)

    @on(RewindPickerOverlay.RewindSelected)
    def _on_rewind_picker_selected(self, event: RewindPickerOverlay.RewindSelected) -> None:
        """Commit the picker's choice — abort + truncate atomically.

        Handler stays thin; the work runs in
        ``_apply_rewind_selection`` so any in-flight turn can be
        cancelled cleanly off the message-handler hot path.
        """
        self._command_dispatcher._actions.run_command(
            self._apply_rewind_selection,
            event.seq,
            event.restored_content,
        )

    async def _apply_rewind_selection(
        self,
        target_seq: int,
        restored_content: str,
    ) -> None:
        """Cancel any in-flight turn, call rewind, restore composer text."""
        session = self._active_session()
        if session is None:
            return
        session_id = session.info.session_id

        # Best-effort abort. If a tool call is mid-flight in a
        # non-cancellable state the rewind still fires; we're deleting
        # the rows the abort was producing anyway. ``_interrupt_turn``
        # is the canonical path — it hides the tool-progress spinner,
        # aborts in-flight tools, drains the queue, and fires a
        # server-side cancel. We still await ``cancel_session`` after
        # so the runtime's busy guard (``rewind_to`` refuses when
        # ``is_busy``) sees the turn fully settled before we truncate.
        if self._turn.is_busy:
            self._interrupt_turn()
            try:
                await self.managed_client.cancel_session(session_id)
            except Exception as exc:
                logger.warning(
                    "Cancel before rewind failed | session={} error={}",
                    session_id[:8],
                    exc,
                )

        try:
            result = await self.managed_client.rewind_session(session_id, from_seq=target_seq)
        except Exception as exc:
            logger.warning(
                "Rewind failed | session={} from_seq={} error={}",
                session_id[:8],
                target_seq,
                exc,
            )
            self._flash(f"Rewind failed: {exc}", severity="error")
            return

        status = result.get("status", "failed")
        if status != "completed":
            reason = result.get("reason", "unknown")
            self._flash(f"Rewind {status}: {reason}", severity="warning")
            return

        deleted_count = int(result.get("deleted_count") or 0)
        # Use the platform-echoed content when present so freshly-written
        # rows (e.g. just-typed user text) survive even if the picker's
        # in-memory copy was a few ms stale. Fall back to the picker's
        # value if the API didn't echo for any reason.
        new_text = str(result.get("restored_content") or restored_content)

        # Reload the truncated transcript so the conversation view
        # matches the new server state.
        await self._sessions_manager.load_transcript(session_id, force=True)
        # Reset per-session TurnState. ``_interrupt_turn`` flipped the
        # global lifecycle to IDLE and marked running tools as errored,
        # but the per-session reducer still carries the cancelled turn's
        # ``tool_runs`` and cumulative draft — and late events that
        # arrived while the cancel was settling could have re-flipped
        # ``phase`` to GENERATING/RUNNING_TOOLS. Without this reset,
        # ``sync_progress_indicator`` sees ``phase=IDLE`` with non-empty
        # ``tool_runs`` and keeps the spinner up as "thinking between
        # tool_end and next generation".
        session.turn_state = TurnState.empty(session_id)
        self._sync_active_session_projection()

        composer = self.query_one("#composer", ComposerInput)
        self._set_composer_text(composer, new_text)
        composer.focus()
        self._flash(
            f"Rewound — {deleted_count} message{'s' if deleted_count != 1 else ''} removed",
            severity="success",
        )

    @work(exclusive=True, group="session-switch")
    async def _switch_session(self, session_id: str) -> None:
        logger.info("Session switch | session={}", session_id[:8])
        self._dismiss_welcome()
        self.active_session_id = session_id
        self._sessions_manager.clear_session_unread(session_id)
        restored_model = self.sessions[session_id].model
        if restored_model != self.model:
            self._on_model_changed(restored_model)

        self.last_input_tokens = 0
        self.tool_call_count = 0
        self.cost_usd = 0.0
        self.cost_unknown = False
        self.subagent_cost_usd = 0.0
        await self._sessions_manager.load_transcript(session_id)
        await self._sync_runtime_session_subscriptions()
        self._sync_active_session_projection()
        self._sync_sessions()
        self._sessions_manager.sync_queue()
        self._update_context()

    async def _resume_requested_session(self) -> None:
        """Resume a session requested via --resume CLI flag.

        When the resume ID is the pick sentinel, open the
        session picker instead of matching a prefix — this is what
        ``dn --resume`` (no ID) resolves to.
        """
        if self._resume_session_id == RESUME_PICK_SENTINEL:
            self._refresh_sessions_then_open_picker()
            return

        prefix = self._resume_session_id or ""
        matches = [sid for sid in self.sessions if sid.startswith(prefix)]

        # No in-memory match: try a direct lookup against the runtime, which
        # also hydrates from the platform / legacy local store on miss. This
        # makes ``--resume <full-id>`` work without first paying for a bulk
        # session refresh.
        if not matches and prefix:
            record = await self._sessions_manager.ensure_session_loaded(prefix)
            if record is not None:
                matches = [record.info.session_id]

        if len(matches) == 1:
            self.active_session_id = matches[0]
            self._sessions_manager.clear_session_unread(matches[0])
            restored_model = self.sessions[matches[0]].model
            if restored_model != self.model:
                self._on_model_changed(restored_model)
            await self._sessions_manager.load_transcript(self.active_session_id)
            self._dismiss_welcome()
            await self._sync_runtime_session_subscriptions()
            self._sync_active_session_projection()
            self._update_context()
        elif len(matches) > 1:
            self.active_session_id = None
            self._sync_conversation()
            await self._sync_runtime_session_subscriptions()
            self._sync_active_session_projection()
            self._flash(
                f"Multiple sessions match '{prefix}' — use a longer prefix", severity="warning"
            )
        else:
            self.active_session_id = None
            self._sync_conversation()
            await self._sync_runtime_session_subscriptions()
            self._sync_active_session_projection()
            self._flash(f"No session found matching '{prefix}'", severity="warning")

    @work(exclusive=True, group="session")
    async def _start_agent_session(self, agent_name: str) -> None:
        if self.runtime_info is None:
            self._flash("Runtime metadata is not loaded", severity="warning")
            return
        available = {"default"} | {
            agent["name"] for agent in self._capabilities_manager.collect_agents()
        }
        if agent_name not in available:
            self._flash(f"Unknown agent: {agent_name}", severity="warning")
            return
        if self._active_session() is None:
            await self._create_new_session_inner(
                agent=None if agent_name == "default" else agent_name
            )
            return
        self._set_active_session_agent(agent_name)

    # ==================================================================
    # Chat
    # ==================================================================

    @work(exit_on_error=False, exclusive=True, group="session")
    async def _send_chat(self, message: str, _user_entry_shown: bool = False) -> None:
        await self._turn_coordinator.send_chat(message, user_entry_shown=_user_entry_shown)

    @work(exit_on_error=False, exclusive=True, group="session")
    async def _execute_shell(self, command: str) -> None:
        await self._turn_coordinator.execute_shell(command)

    @work(exit_on_error=False, exclusive=True, group="session")
    async def _send_chat_to_agent(self, message: str, agent_name: str) -> None:
        await self._turn_coordinator.send_chat_to_agent(message, agent_name)

    # ==================================================================
    # Permission handling
    # ==================================================================

    @work(exit_on_error=False)
    async def _send_permission_response(
        self, request_id: str, decision: str, tool_name: str = ""
    ) -> None:
        await self._turn_coordinator.send_permission_response(
            request_id, decision, tool_name=tool_name
        )

    @work(exit_on_error=False)
    async def _send_human_input_response(
        self,
        request_id: str,
        action: t.Literal["submit", "cancel"],
        *,
        answers: list[QuestionAnswer] | None = None,
    ) -> None:
        await self._turn_coordinator.send_human_input_response(
            request_id,
            action,
            answers=answers,
        )

    # ==================================================================
    # Event handling — delegated to SessionsManager
    # ==================================================================

    def _handle_event(self, event: dict[str, t.Any], session_id: str) -> None:
        self._sessions_manager.handle_event(event, session_id)

    def _cancel_active_prompt(self) -> bool:
        """Cancel the active human prompt if one is present."""
        return self._turn_coordinator.cancel_active_prompt()

    # ==================================================================
    # Command dispatch
    # ==================================================================

    def _handle_command(self, raw: str) -> None:
        self._command_dispatcher.handle_command(raw)

    @work(group="command", exclusive=True)
    async def _run_command(self, coro_fn: t.Callable[..., t.Awaitable[None]], *args: t.Any) -> None:
        """Generic worker for async command implementations."""
        try:
            await coro_fn(*args)
        except AuthenticationError:
            self._profile_manager.handle_authentication_error(
                "Session expired — please sign in again"
            )
        except Exception as exc:
            logger.exception("Command {} failed", getattr(coro_fn, "__name__", coro_fn))
            self._flash(str(exc), severity="warning")

    def _notify_tracked(
        self,
        message: str,
        *,
        title: str = "",
        severity: SeverityLevel = "information",
        timeout: float | None = None,
        markup: bool = True,
    ) -> Notification:
        # Kept as an app-level method because the CapabilitiesScreen and
        # some tests monkeypatch ``app._notify_tracked``/``_dismiss_notification``
        # directly — routing through the dispatcher would break those
        # patches.
        return self._command_dispatcher.notify_tracked(
            message,
            title=title,
            severity=severity,
            timeout=timeout,
            markup=markup,
        )

    def _dismiss_notification(self, notification: Notification | None) -> None:
        self._command_dispatcher.dismiss_notification(notification)

    @work(exclusive=True, group="skills_fetch")
    async def _open_skills_dialog(self) -> None:
        """Fetch skills and open the skills browser below the composer."""
        dialog = self.query_one("#skills-dialog", SkillsDialog)
        if dialog.is_visible:
            dialog.hide()
            return
        try:
            skills = await self.managed_client.fetch_skills()
        except Exception:
            logger.opt(exception=True).warning("Failed to fetch skills for dialog")
            self._flash("Failed to fetch skills", severity="warning")
            return
        if not skills:
            self._flash("No skills available", severity="info")
            return
        composer = self.query_one("#composer", ComposerInput)
        composer.load_text("")
        # Always display the qualified id so the command a user remembers
        # doesn't mutate when another capability ships the same bare name.
        # Bundled skills have no namespace, so their qualified id is bare.
        entries = [(s.qualified_id or s.name, s.description) for s in skills]
        dialog.show_skills(entries)
        composer.focus()

    @on(SkillsDialog.SkillSelected)
    def _on_skill_selected(self, event: SkillsDialog.SkillSelected) -> None:
        """When a skill is selected from the dialog, prefill the composer."""
        composer = self.query_one("#composer", ComposerInput)
        text = f"/{event.skill_name} "
        composer.load_text(text)
        composer.move_cursor_relative(rows=0, columns=len(text))
        composer.focus()

    @staticmethod
    def _model_from_profile(profile: Profile | None) -> str:
        """Resolve the default model from a saved profile."""
        if profile and profile.default_model:
            return profile.default_model
        return DEFAULT_MODEL

    async def _persist_default_model_choice(self, model: str) -> None:
        """Persist an explicit user model selection into the current profile."""
        profile = self._current_profile
        if profile is None or not profile.name or profile.default_model == model:
            return

        updated_profile = profile.model_copy(update={"default_model": model})
        updated_profile._name = profile.name
        self._current_profile = updated_profile
        await asyncio.to_thread(_save_profile, profile.name, updated_profile)

    def action_toggle_output_mode(self) -> None:
        """Toggle output mode between compact and expanded (^O).

        Controls how much detail is shown for tool results and other
        expandable content in the conversation view.
        """
        new_mode: t.Literal["compact", "expanded"] = (
            "expanded" if self.output_mode == "compact" else "compact"
        )
        self.output_mode = new_mode
        from dreadnode.app.tui.widgets.conversation import CompactionSummary, ThinkingBlock
        from dreadnode.app.tui.widgets.tool import ToolCall as ToolCallWidget

        # ^O drives every expandable surface: tool output, compaction summaries,
        # and reasoning. Reasoning was previously excluded (ENG-6108) but that
        # left long traces filling the viewport with no way to shorten them, so
        # ^O now shortens/expands ThinkingBlocks too (ENG-7463).
        try:
            conv = self.query_one("#conversation", ConversationView)
            for tc in conv.query(ToolCallWidget):
                tc.refresh(layout=True)
            expanded = new_mode == "expanded"
            for cs in conv.query(CompactionSummary):
                cs.display = expanded
            for tb in conv.query(ThinkingBlock):
                tb.set_output_mode(new_mode)
        except Exception:
            logger.debug("Could not refresh output mode widgets")
        self._flash(f"Output: {new_mode}", severity="info")

    @work(exclusive=True, group="tools_fetch")
    async def _open_tools_dialog(self) -> None:
        """Show the tools browser dialog, refreshing the catalog if empty."""
        dialog = self.query_one("#tools-dialog", ToolsDialog)
        if dialog.is_visible:
            dialog.hide()
            return
        # Prefer the manager's cached catalog — populated by refresh().
        # Fall back to an on-demand fetch if the cache is empty (e.g.
        # the dialog is opened before the first runtime refresh lands).
        tools = list(self._capabilities_manager.tool_catalog.values())
        if not tools:
            try:
                fetched = await self.managed_client.fetch_tools()
            except Exception:
                logger.opt(exception=True).warning("Failed to fetch tools for dialog")
                self._flash("Failed to fetch tools", severity="warning")
                return
            self._capabilities_manager.set_tool_catalog(fetched)
            tools = fetched
        dialog.show_tools(tools)

    def _on_workspace_screen_dismiss(self, result: "SwitchRequest | None") -> None:
        """Handle workspace/project switch request from WorkspaceScreen."""
        if result is None:
            return
        self._do_context_switch(result)

    @work(exclusive=True, group="context_switch")
    async def _do_context_switch(self, request: "SwitchRequest") -> None:
        """Execute a full context switch: update profile, restart runtime."""
        try:
            profile_name, profile = _active_profile()
        except Exception as exc:
            self._flash(str(exc), severity="warning")
            return
        if profile_name is None or profile is None:
            self._flash("Not logged in. Use /login first.", severity="warning")
            return

        org_key = request.org_key
        workspace_key = request.workspace_key
        project_key = request.project_key

        # If no explicit project, resolve the default for the target workspace
        if not project_key:
            try:
                api, _ = await asyncio.to_thread(_platform_client)
                project_key = await asyncio.to_thread(
                    api.get_default_project_key, org_key, workspace_key
                )
            except Exception:
                project_key = None

        # Check if anything actually changed
        if (
            profile.default_organization == org_key
            and profile.default_workspace == workspace_key
            and profile.default_project == project_key
        ):
            self._flash("Already on this context", severity="info")
            return

        # Update profile
        updated_profile = profile.model_copy(
            update={
                "default_organization": org_key,
                "default_workspace": workspace_key,
                "default_project": project_key,
            }
        )

        try:
            await asyncio.to_thread(_save_profile, profile_name, updated_profile)
        except Exception as exc:
            self._flash(f"Failed to save profile: {exc}", severity="error")
            return

        # ProfileManager.apply_auth_profile handles session clearing via restart() → reset_app_state()
        await self._profile_manager.apply_auth_profile(updated_profile)
        self._flash(
            f"Switched to {workspace_key}/{project_key or 'default'}",
            severity="success",
        )

    def _on_capabilities_dismiss(self, _result: t.Any) -> None:
        """Refresh runtime info after capabilities screen closes.

        If the capabilities screen set a pending fix message, create a new
        session and send the diagnostic message to the agent.
        """
        message = self._capabilities_manager.take_pending_fix_message()
        if message:
            self._dismiss_welcome()
            self._send_chat(message)
            return
        self._run_command(self._capabilities_manager.refresh)

    # ==================================================================
    # Prompt history
    # ==================================================================

    def _load_prompt_history(self) -> None:
        """Load prompt history from persistent JSONL file."""
        try:
            if not _HISTORY_FILE.is_file():
                return
            entries: list[str] = []
            for raw_line in _HISTORY_FILE.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    text = json.loads(line).get("text", "")
                except (json.JSONDecodeError, AttributeError):
                    logger.debug("Skipping malformed history entry")
                    continue
                if text and (not entries or entries[-1] != text):
                    entries.append(text)
            self._prompt_history = entries[-_MAX_HISTORY:]
        except OSError:
            logger.opt(exception=True).debug("Could not read prompt history file")

    def _save_prompt_entry(self, text: str) -> None:
        """Append a single prompt entry to the persistent history file."""
        try:
            _HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with _HISTORY_FILE.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"text": text}) + "\n")
        except OSError:
            logger.opt(exception=True).debug("Could not write prompt history entry")

    def _history_navigate(self, direction: int) -> None:
        """Navigate prompt history. direction: -1 for up, 1 for down."""
        if not self._prompt_history:
            return
        composer = self.query_one("#composer", ComposerInput)

        if self._history_index == -1:
            if direction == -1:
                self._history_stash = composer.value
                self._history_index = len(self._prompt_history) - 1
            else:
                return
        else:
            new_index = self._history_index + direction
            if new_index < 0:
                return
            if new_index >= len(self._prompt_history):
                self._history_index = -1
                self._set_composer_text(composer, self._history_stash)
                return
            self._history_index = new_index

        self._set_composer_text(composer, self._prompt_history[self._history_index])

    def _set_composer_text(self, composer: ComposerInput, text: str) -> None:
        """Replace composer text and move cursor to end."""
        composer.clear_pastes()
        composer.load_text(text)
        end = composer.document.end
        composer.move_cursor(end)

    # ==================================================================
    # Copy and export
    # ==================================================================

    def copy_to_clipboard(self, text: str) -> None:
        """Copy text to the OS clipboard via OSC 52 with a CLI fallback.

        Overrides Textual's default ``App.copy_to_clipboard`` (OSC-52-only)
        so every framework path that ends up here — ``screen.copy_text``
        fired by Ctrl+C, ``TextArea.action_copy``, our own ``y`` handler,
        the console screen's log copy — also tries native clipboard CLIs
        when OSC 52 isn't honored. Many terminals silently drop OSC 52:
        macOS Terminal.app, gnome-terminal (default), xterm, konsole on
        some configs. Without the CLI fallback Ctrl+C looks like a no-op
        on those terminals even though the keystroke fired correctly.

        Fallback chain:
            macOS                  -> pbcopy
            Linux X11              -> xclip, then xsel
            Linux Wayland          -> wl-copy

        Headless / SSH'd sessions with no clipboard CLI installed will
        still no-op silently; users on those setups need OSC 52 enabled
        in their terminal/multiplexer, or one of the CLI tools installed.
        """
        import shutil
        import subprocess
        import sys

        # Sanitize: replace unrepresentable characters so encode() never raises
        safe_text = text.encode("utf-8", errors="replace").decode("utf-8")

        # OSC 52 first — fast path on iTerm2, WezTerm, Kitty, Ghostty, etc.
        with contextlib.suppress(Exception):
            super().copy_to_clipboard(safe_text)

        # Native clipboard CLI fallback — covers Terminal.app, gnome-terminal,
        # xterm, and any other terminal that drops OSC 52 by default.
        if sys.platform == "darwin":
            cmd = "pbcopy"
        elif shutil.which("xclip"):
            cmd = "xclip -selection clipboard"
        elif shutil.which("xsel"):
            cmd = "xsel --clipboard --input"
        elif shutil.which("wl-copy"):
            cmd = "wl-copy"
        else:
            return
        with contextlib.suppress(subprocess.SubprocessError, FileNotFoundError, OSError):
            subprocess.run(  # noqa: S603 - command is selected from a fixed local allowlist
                cmd.split(),
                input=safe_text.encode("utf-8"),
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    def _copy_last_assistant(self) -> None:
        """Copy the last assistant message to clipboard."""
        session = self._active_session()
        if session is None:
            return
        for entry in reversed(session.transcript):
            if entry.role == "assistant" and not entry.metadata.get("thinking"):
                self.copy_to_clipboard(entry.content or "")
                self._flash("Copied to clipboard", severity="success")
                return
        self._flash("No assistant message to copy", severity="warning")

    @work(group="command", exclusive=True)
    async def _export_session(self, filename: str | None = None) -> None:
        """Export session transcript to a markdown file."""
        session = self._active_session()
        if session is None:
            self._flash("No active session to export", severity="warning")
            return

        if filename is None:
            sid_prefix = session.info.session_id[:8]
            filename = f"session-{sid_prefix}.md"

        lines: list[str] = []
        title = session.info.session_id[:8]
        lines.append(f"# {title}\n")

        for entry in session.transcript:
            content = entry.content or ""
            meta = entry.metadata
            if entry.role == "user":
                lines.append(f"> {content}\n")
            elif entry.role == "assistant" and not meta.get("thinking"):
                lines.append(f"{content}\n")
            elif entry.role == "tool":
                tool_name = meta.get("tool_name") or "tool"
                lines.append(f"```\n{tool_name}: {content}\n```\n")
            elif entry.role == "system" and meta.get("error"):
                lines.append(f"**Error:** {content}\n")

        content = "\n".join(lines)
        try:
            Path(filename).write_text(content, encoding="utf-8")
            self._flash(f"Exported to {filename}", severity="success")
        except Exception as exc:
            self._flash(f"Export failed: {exc}", severity="error")

    # ==================================================================
    # Session title
    # ==================================================================

    def _rename_session(self, new_title: str) -> None:
        """Rename the active session.

        Updates ``info.title`` optimistically so the UI reflects the
        rename instantly, then persists to the platform in a worker. If
        the worker fails the user sees an error toast; the next refresh
        will reset ``info.title`` to whatever the platform has.
        """
        session = self._active_session()
        if session is None:
            self._flash("No active session to rename", severity="warning")
            return
        logger.info("Session rename | session={} title={}", session.info.session_id[:8], new_title)
        session.info.title = new_title
        self._sync_sessions()
        self._update_context()
        self._flash(f"Session renamed to '{new_title}'", severity="success")
        self.run_worker(
            self._persist_session_title(session.info.session_id, new_title),
            exit_on_error=False,
            exclusive=True,
            group=f"rename-session-{session.info.session_id}",
        )

    async def _persist_session_title(self, session_id: str, title: str) -> None:
        """Push the renamed session title to the runtime server."""
        try:
            await self.managed_client.set_session_title(session_id, title)
        except Exception as exc:
            logger.opt(exception=True).warning("Failed to persist session title")
            self._flash(f"Failed to sync session title: {exc}", severity="error")

    # ==================================================================
    # Internal helpers
    # ==================================================================

    def _active_session(self) -> SessionRecord | None:
        if self.active_session_id is None:
            return None
        return self.sessions.get(self.active_session_id)

    def _is_active_session(self, session_id: str) -> bool:
        return self.active_session_id == session_id

    async def _sync_runtime_session_subscriptions(self) -> None:
        await self._sessions_manager.sync_runtime_session_subscriptions()

    def _schedule_runtime_session_subscription_sync(self) -> None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return

        async def _do_sync() -> None:
            await self._sync_runtime_session_subscriptions()

        # RUF006: fire-and-forget — subscription sync is best-effort and the
        # caller does not need to await or cancel it.
        loop.create_task(_do_sync())  # noqa: RUF006

    def _sync_active_session_projection(self) -> None:
        self._sessions_manager.sync_active_session_projection()

    def _set_active_session_agent(self, agent_name: str) -> None:
        """Update the active session's primary agent without recreating the session."""
        session = self._active_session()
        if session is None:
            return
        if agent_name == "default":
            resolved_default_agent = self._capabilities_manager.default_agent_name()
            resolved_default_capability = self._capabilities_manager.default_capability_name()
            session.info.agent = resolved_default_agent
            session.info.capability = resolved_default_capability
            self._sync_sessions()
            self._update_context()
            return
        session.info.agent = agent_name
        capability_name = self._capabilities_manager.capability_for_agent(agent_name)
        if capability_name is not None:
            session.info.capability = capability_name
        self._sync_sessions()
        self._update_context()

    def _append_transcript(self, entry: Message, session_id: str, *, scroll: bool = True) -> None:
        """Append an entry to a session's transcript.

        Kept as a real method on the app (not a delegation) so that tests
        which patch ``app._append_transcript = MagicMock()`` still work —
        :class:`SessionsManager` reaches this through
        :class:`_AppSessionsUi.append_transcript`, which looks up the method
        at call time.

        The conversation-view append is synchronous so widgets land in the
        same order their events arrived. A deferred ``call_after_refresh``
        used to reorder entries against the synchronous tool-call mounts
        in :class:`SessionsManager.handle_event` (e.g. an assistant draft
        committed by ``ToolStart`` would land *after* the tool row).
        """
        record = self.sessions.get(session_id)
        if record is None:
            return
        record.transcript.append(entry)
        if self.active_session_id == session_id:
            conv = self.query_one("#conversation", ConversationView)
            conv.append_entry(entry, scroll=scroll)

    def _sync_conversation(self) -> None:
        self._sessions_manager.sync_conversation()

    def _sync_sessions(self) -> None:
        """Kept as a no-op — session state is shown via the session picker screen."""

    def _on_model_changed(self, new_model: str) -> None:
        """Restore per-model variant state after model switch."""
        self.model = new_model
        active = self._active_session()
        if active is not None:
            active.model = new_model
        if new_model in self._model_variants:
            # User has an explicit preference for this model (including "" for off)
            stored = self._model_variants[new_model]
            if stored:
                from dreadnode.app.tui.model_variants import get_variants

                variants = get_variants(new_model)
                if stored in variants:
                    self.thinking_enabled = True
                    self.effort_label = stored
                else:
                    # Model doesn't support this variant anymore
                    del self._model_variants[new_model]
                    self.thinking_enabled = False
                    self.effort_label = ""
            else:
                # User explicitly disabled thinking for this model
                self.thinking_enabled = False
                self.effort_label = ""
        else:
            # First time seeing this model — apply sane default
            from dreadnode.app.tui.model_variants import default_effort

            fallback = default_effort(new_model)
            if fallback:
                self.thinking_enabled = True
                self.effort_label = fallback
                self._model_variants[new_model] = fallback
            else:
                self.thinking_enabled = False
                self.effort_label = ""
        self._update_context()

    # ==================================================================
    # Session state stash/restore (for runtime switching)
    # ==================================================================

    def _restore_session_state(self, bundle: "SessionStateBundle") -> None:
        """Restore a stashed session bundle after a runtime swap.

        Pure session-state restoration lives on :class:`SessionsManager`;
        this wrapper runs the two app-scoped follow-ups the manager
        can't see: refreshing the remote/local status indicator and
        kicking off a background subscription reconcile.
        """
        self._sessions_manager.restore_state(bundle)
        self._update_remote_status()
        self._schedule_runtime_session_subscription_sync()

    async def _on_remote_connected(self) -> None:
        """Called after RuntimeConnectionManager.connect() succeeds.

        Clears local session state from the UI, refreshes runtime info and
        sessions from the remote server, and updates the status bar.
        """
        # Clear local sessions/state from the UI (local bundle is already stashed)
        self.sessions = {}
        self.active_session_id = None

        # Re-point the notify subscriber at the remote runtime so toasts
        # emitted by remote workers render here. The exclusive worker group
        # cancels the local-client subscriber.
        self._install_notify_subscriber(self._connection_manager.active_client)

        # Refresh from the remote server. The user lands on the welcome
        # screen with the remote's session list visible in the sidebar; the
        # first turn they send creates a session on demand via
        # ``ensure_active_session``.
        await self._capabilities_manager.refresh()
        await self._refresh_server_sessions()

        self._update_remote_status()
        self._sync_conversation()
        if self.active_session_id is not None:
            self._dismiss_welcome()

    async def _on_remote_disconnected(self) -> None:
        """Called after RuntimeConnectionManager.disconnect() succeeds.

        Local session state is already restored by on_restore_state callback.
        This refreshes runtime info from the local server and updates the UI.
        """
        self._install_notify_subscriber(self._connection_manager.local_client)
        await self._capabilities_manager.refresh()
        await self._refresh_server_sessions()
        self._update_remote_status()
        self._sync_conversation()

    def _update_remote_status(self) -> None:
        """Update status bar to reflect remote/local connection state."""
        if self._connection_manager.is_remote:
            info = self._connection_manager.connection_info
            if info:
                self.remote_info = f"remote · {info.runtime_id[:8]}"
            else:
                self.remote_info = "remote"
        else:
            self.remote_info = ""

    def _install_notify_subscriber(self, client: ManagedRuntimeClient) -> None:
        """Run a background ``client.subscribe("notify")`` loop for toasts.

        Uses an exclusive worker group so switching clients (local ↔ remote)
        cancels the prior subscriber — the iterator's ``finally`` closes the
        socket and releases the server-side bus subscription.
        """
        self.run_worker(
            self._notify_subscriber_loop(client),
            exit_on_error=False,
            exclusive=True,
            group="notify-subscriber",
        )
        self.run_worker(
            self._component_subscriber_loop(client),
            exit_on_error=False,
            exclusive=True,
            group="component-subscriber",
        )

    async def _notify_subscriber_loop(self, client: ManagedRuntimeClient) -> None:
        """Consume ``notify`` envelopes from *client* and render them as toasts.

        ``RuntimeClient.subscribe`` handles transient transport reconnects
        internally (CAP-WCLI-021); this outer loop only exists to survive
        server-startup races where the first connect attempt fails before
        the local runtime is up.

        Wait for the runtime to be started before calling ``subscribe`` —
        ``subscribe`` would otherwise call ``start()`` itself and race
        ``ProfileManager.boot``, booting the in-process server twice
        (and the first boot with empty platform credentials).
        """
        await client.wait_until_started()
        backoff = 0.5
        while True:
            try:
                async for envelope in client.subscribe("notify"):
                    # CAP-WCLI-021: the client yields a ``transport.reconnected``
                    # envelope after each auto-reconnect regardless of the
                    # subscription filter. It is not a user-facing notification,
                    # so skip it — worker-published notify events emitted
                    # during the disconnect are not replayed (CAP-WCLI-020).
                    if envelope.kind == "transport.reconnected":
                        logger.debug(
                            "Notify subscriber: transport reconnected | kinds={}",
                            envelope.payload.get("kinds"),
                        )
                        continue
                    self._render_notify_envelope(envelope)
            except asyncio.CancelledError:
                raise
            except AuthenticationError:
                logger.opt(exception=True).warning(
                    "Notify subscriber: authentication failed; not retrying"
                )
                return
            except Exception:
                logger.opt(exception=True).debug(
                    "Notify subscriber transient failure | backoff={:.1f}s",
                    backoff,
                )
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 5.0)

    async def _component_subscriber_loop(self, client: ManagedRuntimeClient) -> None:
        """Consume ``component.state_changed`` envelopes and patch live state.

        Mirrors ``_notify_subscriber_loop``'s reconnect/backoff shape. On
        each envelope we patch the cached ``runtime_info`` snapshot in
        place (so the page-status zone, services screen, and any other
        consumer pick up fresh status without a polling round-trip),
        then post a :class:`ComponentStateChanged` Textual message so
        open screens can re-render their cached views.
        """
        await client.wait_until_started()
        backoff = 0.5
        while True:
            try:
                async for envelope in client.subscribe(EVENT_COMPONENT_STATE_CHANGED):
                    if envelope.kind == "transport.reconnected":
                        # We may have missed events while disconnected —
                        # re-pull runtime_info so the snapshot resyncs.
                        try:
                            await self._capabilities_manager.refresh()
                        except Exception:
                            logger.opt(exception=True).debug(
                                "Component subscriber: post-reconnect refresh failed"
                            )
                        continue
                    if envelope.kind != EVENT_COMPONENT_STATE_CHANGED:
                        continue
                    self._apply_component_state_envelope(envelope)
            except asyncio.CancelledError:
                raise
            except AuthenticationError:
                logger.opt(exception=True).warning(
                    "Component subscriber: authentication failed; not retrying"
                )
                return
            except Exception:
                logger.opt(exception=True).debug(
                    "Component subscriber transient failure | backoff={:.1f}s",
                    backoff,
                )
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 5.0)

    def _apply_component_state_envelope(self, envelope: RuntimeEventEnvelope) -> None:
        """Patch ``runtime_info`` in place and notify open screens."""
        payload = envelope.payload or {}
        patched = self._capabilities_manager.apply_component_state_change(payload)
        if not patched:
            # Snapshot didn't know about this component — typical during
            # startup races. The next refresh will reconcile.
            return
        # Re-derive runtime_health groups so the page-status indicator
        # picks up the new status without waiting for a full refresh.
        self._capabilities_manager.update_runtime_health()
        self.post_message(ComponentStateChanged(payload))

    def _render_notify_envelope(self, envelope: RuntimeEventEnvelope) -> None:
        """Render a ``notify`` envelope (CAP-WEVT-004) as a Textual toast."""
        payload = envelope.payload
        title = str(payload.get("title") or "")
        if not title:
            # CAP-WEVT-004 requires ``title``; drop malformed emissions so
            # we don't flash empty toasts.
            return
        body = payload.get("body")
        source = str(payload.get("source") or "")
        severity = str(payload.get("severity") or "info")
        # Textual's notify severity is ``information|warning|error``; our
        # spec adds ``success``, which we also render as ``information``.
        textual_severity = {
            "info": "information",
            "warning": "warning",
            "error": "error",
            "success": "information",
        }.get(severity, "information")
        # Match the conventional shape used by screens in this app: the
        # source becomes the toast title (category), the emitted title is
        # the short message, and ``body`` adds detail if present.
        message = title if not isinstance(body, str) or not body else f"{title}\n{body}"
        self.notify(
            message,
            title=source or "Notification",
            severity=textual_severity,
        )

    def _update_context(self) -> None:
        active = self._active_session()
        if active:
            # Single-line slot next to @agent: render only the title (the
            # preview belongs alongside the title in list views, not in
            # the always-visible context bar). Cap the displayed title so
            # a long title can't push model / token info off the right.
            title = active.display_title().strip().replace("\n", " ")
            if len(title) > 40:
                title = title[:39].rstrip() + "…"
            base_label = title
            # Policy metadata drives the status tag. ``policy_name`` is
            # just the registry key — the *user-facing label* is
            # ``policy_display_label`` (e.g. ``"auto"``, ``"strict"``)
            # and ``policy_is_autonomous`` gates whether we show the
            # tag at all. Capability authors shipping their own
            # policies set both via class vars; the TUI never has to
            # know about specific names.
            if getattr(active.info, "policy_is_autonomous", False):
                display = (
                    getattr(active.info, "policy_display_label", "") or active.info.policy_name
                )
                self.session_label = f"[{display}] {base_label}"
            else:
                self.session_label = base_label
            self.agent_name = self._capabilities_manager.session_display_agent(active.info)
        else:
            self.session_label = "none"
            self.agent_name = self._capabilities_manager.default_agent_name() or "default"
        if self._connection_manager.is_remote:
            info = self._connection_manager.connection_info
            self.connection = f"remote · {info.runtime_id[:8]}" if info else "remote"
        elif self.server_url is not None:
            from urllib.parse import urlparse

            hostname = urlparse(self.server_url).hostname or self.server_url
            self.connection = f"remote · {hostname}"
        else:
            self.connection = "local"
        self.model_name = self.model
        self.background_status = self._sessions_manager.background_session_status()
        try:
            _name, profile = _active_profile()
        except Exception:
            logger.opt(exception=True).debug("Could not load profile for context update")
            profile = None
        if profile and profile.default_workspace:
            if profile.default_project:
                self.workspace_label = f"{profile.default_workspace}/{profile.default_project}"
            else:
                self.workspace_label = profile.default_workspace
        else:
            self.workspace_label = ""

    def _dismiss_welcome(self) -> None:
        """Hide the welcome screen and show the conversation."""
        welcome = self.query_one("#welcome", Welcome)
        if welcome.is_visible:
            welcome.dismiss()
            self.query_one("#conversation", ConversationView).display = True

    def _show_welcome(self) -> None:
        """Re-show the welcome screen and hide the conversation view.

        Used when the user lands back in a sessionless state — e.g. after
        deleting every session in the picker — so the conversation pane
        doesn't read as a half-loaded transcript.
        """
        welcome = self.query_one("#welcome", Welcome)
        if not welcome.is_visible:
            welcome.restore()
            self.query_one("#conversation", ConversationView).display = False

    def _set_composer_enabled(self, enabled: bool) -> None:
        """Toggle composer and its visual state."""
        try:
            self.query_one("#composer", ComposerInput).disabled = not enabled
            bar = self.query_one("#composer-bar")
        except Exception:
            return
        if enabled:
            bar.remove_class("-disabled")
        else:
            bar.add_class("-disabled")

    def _set_connection_status(self, text: str) -> None:
        """Set a terminal connection status shown in the StatusBar (Zone 4).

        Use for connection-level problems (auth required, connection failed).
        Cleared automatically when ``runtime_connected`` becomes True.
        """
        self.connection_status = text

    def _set_boot_status(self, text: str) -> None:
        """Set pre-connect progress shown in the bottom StatusBar."""
        self.boot_status = text

    def _set_status(self, text: str, *, busy: bool | None = None) -> None:
        self.status_text = text
        if busy is not None:
            self.busy = busy

    def _flash(self, message: str, *, severity: str = "info") -> None:
        self.call_after_refresh(self.query_one("#flash", Flash).flash, message, severity=severity)

    def on_connection_error_screen_retry_requested(self) -> None:
        """Handle retry from ConnectionErrorScreen — schedule _boot()."""
        self.call_later(self._profile_manager.schedule_boot)

    def on_connection_error_screen_profile_switch_requested(self) -> None:
        """Handle profile switch from ConnectionErrorScreen — dismiss and open profile picker."""
        self._profile_manager.request_connection_error_profile_switch()

    def _write_activity(self, message: str, *, style: str = "info") -> None:
        """Write an activity message inline in the conversation."""
        color = {
            "info": FG_MUTED,
            "success": FG_MUTED,
            "warning": WARNING,
            "error": ERROR,
        }.get(style, FG_MUTED)
        self.call_after_refresh(
            self.query_one("#conversation", ConversationView).write_system,
            message,
            style=color,
        )

    def _write_agent_output_pointer(self, session_id: str) -> None:
        """Drop a clickable end-of-turn pointer to the web Agent Output page
        when the just-finished turn reported any structured items.

        Skips silently when the turn reported nothing, when the session isn't
        the visible one (the line would land in a hidden conversation), or
        when there's no platform link to offer (local / unauthenticated). The
        per-row links scroll away in a long session; this leaves one standing
        pointer at the foot of the turn that produced output.
        """
        if session_id != self.active_session_id:
            return
        state = self._sessions_manager.session_turn_state(session_id)
        if state is None:
            return
        reported = sum(
            1
            for run in state.tool_runs.values()
            if run.tool_name == "report_item" and run.persisted
        )
        if reported == 0:
            return
        record = self.sessions.get(session_id)
        project = record.info.project if record else None
        url = self._build_agent_output_url(project)
        if url is None:
            return

        from rich.style import Style
        from rich.text import Text

        from dreadnode.app.tui.widgets.tool import AGENT_OUTPUT_URL_LABEL

        noun = "item" if reported == 1 else "items"
        text = Text()
        text.append("↗ ", style=FG_MUTED)
        text.append(f"{reported} {noun} reported · ", style=FG_MUTED)
        text.append(
            AGENT_OUTPUT_URL_LABEL,
            style=Style.from_meta({"@click": f"open_url({url!r})"}),
        )
        self.query_one("#conversation", ConversationView).write(text)

    def _show_help(self) -> None:
        """Write help content inline into the conversation view."""
        self._dismiss_welcome()
        conv = self.query_one("#conversation", ConversationView)
        conv.write(render_help())

    def _write_session_listing(self) -> None:
        """Write formatted session list inline in the conversation."""
        from rich.text import Text as RichText

        if not self.sessions:
            self._flash("No active sessions", severity="warning")
            return

        conversation = self.query_one("#conversation", ConversationView)
        header = RichText()
        header.append("· ", style=INFO)
        header.append(f"Sessions ({len(self.sessions)})", style=f"bold {INFO}")
        conversation.write(header)

        for sid in sorted(self.sessions.keys(), reverse=True):
            rec = self.sessions[sid]
            display = rec.display_title()
            line = RichText()
            is_active = sid == self.active_session_id
            line.append("  ● " if is_active else "  ○ ", style=ACCENT if is_active else FG_FAINTEST)
            line.append(f"{display:<20}", style=FG if is_active else FG_SUBTLE)
            line.append(self._capabilities_manager.session_display_agent(rec.info), style=FG_MUTED)
            line.append(f"  {rec.info.message_count} msgs", style=FG_FAINTEST)
            line.append(f"  {sid[:8]}", style=FG_FAINTEST)
            conversation.write(line)

    def _write_agent_listing(self) -> None:
        """Write formatted agent list inline in the conversation."""
        if self.runtime_info is None:
            self._flash("Runtime not loaded", severity="warning")
            return
        if not any(c.agents for c in self.runtime_info.capabilities):
            self._flash("No agents loaded", severity="warning")
            return

        # On the home screen the conversation is hidden behind the welcome
        # card; reveal it so the listing is actually visible instead of being
        # written into an off-screen view.
        self._dismiss_welcome()
        conversation = self.query_one("#conversation", ConversationView)
        for line in _build_agent_listing(self.runtime_info.capabilities, self.agent_name):
            conversation.write(line)
