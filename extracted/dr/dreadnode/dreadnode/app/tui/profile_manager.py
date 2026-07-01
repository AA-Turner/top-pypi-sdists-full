"""Profile management, auth flow, and boot/login/logout orchestration.

This module used to contain a single 669-line ``ProfileManager`` class that
owned every profile lifecycle concern the TUI had: the auth modal UI, the
connection-error modal UI, the profile picker, applying a profile to the
runtime, booting from a persisted profile, validating credentials, logging
in, logging out, switching profiles, and auth error recovery. That single
class was the primary example cited in ``docs/later/TUI_MANAGER_DECOUPLING.MD``
of a "manager that is still a god controller under a new name".

Per Phase 5 of that plan, the implementation is now split into three
collaborators, each responsible for one cohesive lifecycle:

- :class:`AuthModalController` — owns the auth modal, the connection-error
  modal, the profile picker dialog, and banner updates. Purely UI-shaped.
- :class:`ProfileRuntimeController` — owns the runtime-facing side-effects
  of applying a connected profile: platform API context setup, local
  runtime restart, platform/model refresh, and initial session bootstrap.
- :class:`BootAndAuthRecoveryController` — owns the boot flow, API key
  validation with backoff, profile switching, login/logout, and auth
  error transitions. Orchestrates the other two.

:class:`ProfileManager` stays in this module as a thin composition facade
that wires the three controllers together and delegates each public method
to the appropriate one. App and test code continues to call
``ProfileManager`` through the same public surface as before — the only
difference is that the behavior now lives in three testable units with
clearly scoped responsibilities.

Cross-controller dependencies (for example: the boot controller calling
into the auth modal controller to show the modal, or the runtime controller
calling back into the boot controller on authentication failure) are
passed as lambdas that look up the facade method at *call time*. This
preserves the existing test pattern where tests patch methods on the
manager instance (e.g. ``manager.show_auth_modal = lambda ...``) — the
late binding ensures the patched version is what actually runs, even from
inside a sub-controller.
"""

import asyncio
import contextlib
import time
import typing as t
from dataclasses import dataclass

import httpx
from loguru import logger

from dreadnode.app.api.client import ApiClient, AuthenticationError
from dreadnode.app.config import Profile, UserConfig
from dreadnode.app.tui.auth_flow import (
    _login_with_api_key,
    _parse_login_args,
)
from dreadnode.app.tui.screens.auth import AuthModal
from dreadnode.app.tui.screens.connection_error import ConnectionErrorScreen
from dreadnode.app.tui.status_messages import (
    STATUS_AUTH_REQUIRED,
    STATUS_AUTHENTICATING,
    STATUS_CONNECTION_FAILED,
    STATUS_LOADING_CAPABILITIES,
    STATUS_LOGGING_IN,
    STATUS_READY,
    STATUS_RESTARTING,
    STATUS_STARTING,
    STATUS_SYNCING,
)

if t.TYPE_CHECKING:
    from dreadnode.app.tui.update_check import UpdateInfo


def _log_background_boot_failure(task: "asyncio.Task[t.Any]") -> None:
    """Surface exceptions from a detached runtime-boot task.

    When early auth failures cause ``boot()`` to return before awaiting
    the runtime-boot task, the task keeps running in the background so
    a subsequent successful auth can reuse it. Without a done-callback,
    any exception raised by the detached task would be lost at GC time
    as ``Task exception was never retrieved``.
    """
    if task.cancelled():
        return
    exc = task.exception()
    if exc is not None:
        logger.opt(exception=exc).debug("Background runtime boot failed")


# =============================================================================
# Shared flow state + ports
# =============================================================================


@dataclass(slots=True)
class ProfileFlowState:
    """Mutable state shared across controllers for in-flight profile flows."""

    switching_profile: bool = False


class ProfileStatePort(t.Protocol):
    def current_profile(self) -> Profile | None: ...

    def set_current_profile(self, profile: Profile) -> None: ...

    def server_url(self) -> str: ...

    def update_available(self) -> str: ...

    def set_authenticated(self, value: bool) -> None: ...

    def set_runtime_connected(self, value: bool) -> None: ...

    def set_model(self, model_id: str) -> None: ...

    def resume_session_id(self) -> str | None: ...

    def active_session_id(self) -> str | None: ...

    def set_active_session_id(self, session_id: str | None) -> None: ...

    def consume_initial_inputs(
        self,
    ) -> tuple[str | None, str | None, dict[str, t.Any] | None]: ...


class ProfileUiPort(t.Protocol):
    def flash(self, message: str, *, severity: str) -> None: ...

    def write_activity(self, message: str, *, style: str = "info") -> None: ...

    def set_status(self, text: str, *, busy: bool | None = None) -> None: ...

    def set_boot_status(self, text: str) -> None: ...

    def set_connection_status(self, text: str) -> None: ...

    def set_composer_enabled(self, enabled: bool) -> None: ...

    def sync_conversation(self) -> None: ...

    def update_context(self) -> None: ...

    def dismiss_welcome(self) -> None: ...


class ProfileScreenPort(t.Protocol):
    def profile_dialog_visible(self) -> bool: ...

    def hide_profile_dialog(self) -> None: ...

    def show_profile_dialog(
        self,
        servers: dict[str, Profile],
        active_name: str | None,
    ) -> None: ...

    def dismiss_pushed_screens(self) -> None: ...

    def current_screen(self) -> object: ...

    def push_screen(
        self,
        screen: object,
        callback: t.Callable[[t.Any], None] | None = None,
    ) -> None: ...

    def focus_composer(self) -> None: ...

    def exit_app(self) -> None: ...

    def update_auth_banner(self, banner: str) -> None: ...


class ProfileRuntimePort(t.Protocol):
    def set_api_context(self, api: ApiClient, organization: str, workspace: str) -> None: ...

    def set_platform_profile(self, profile: Profile) -> None: ...

    def clear_platform_profile(self) -> None: ...

    def local_runtime_started(self) -> bool: ...

    async def start_local_runtime(self) -> None: ...

    async def restart_local_runtime(self) -> None: ...

    async def refresh_runtime(self) -> None: ...

    async def refresh_server_sessions(self, *, include_platform: bool = False) -> None: ...

    async def refresh_skill_names(self) -> None: ...

    async def resume_requested_session(self) -> None: ...

    async def create_new_session(
        self,
        agent: str | None = None,
        *,
        policy: dict[str, t.Any] | None = None,
    ) -> None: ...

    def send_chat(self, message: str) -> None: ...

    def collect_agents(self) -> list[dict[str, str]]: ...


class ProfileModelPort(t.Protocol):
    def clear_platform_proxy_state(self) -> None: ...

    async def refresh_platform_models_and_key(self, api: ApiClient) -> None: ...

    def model_from_profile(self, profile: Profile | None) -> str: ...


class ProfileStorePort(t.Protocol):
    def read_user_config(self) -> UserConfig: ...

    def active_profile_name(self) -> str | None: ...

    def delete_profile(self, profile_name: str) -> bool: ...

    def activate_profile(self, profile_name: str) -> None: ...

    def save_profile(self, profile: Profile) -> None: ...

    def set_in_memory_profile(self, profile_name: str | None, profile: Profile) -> None: ...

    def clear_in_memory_profile(self) -> None: ...

    def active_profile(self) -> tuple[str | None, Profile | None]: ...

    def disconnect_profile(self) -> str | None: ...


class ProfileAsyncActions(t.Protocol):
    def run_exclusive(self, coro: t.Awaitable[t.Any], *, group: str) -> None: ...

    def run_command(
        self,
        coro_fn: t.Callable[..., t.Awaitable[t.Any]],
        *args: t.Any,
    ) -> None: ...


# Cross-controller callback types — used by the facade to wire controllers
# together at composition time without forcing any of them to know about the
# others' concrete classes.
_ShowAuthModal = t.Callable[..., None]
_RetryBoot = t.Callable[[], None]
_ApplyProfile = t.Callable[[Profile], t.Awaitable[bool]]
_HandleAuthError = t.Callable[[str], None]
_EnterConnectionFailed = t.Callable[[str], None]
_DismissConnectionErrorScreen = t.Callable[[], None]
_OpenProfileDialog = t.Callable[[], None]


# =============================================================================
# AuthModalController
# =============================================================================


class AuthModalController:
    """Owns the auth modal, connection-error modal, and profile picker.

    This controller is purely UI-shaped. It never starts a runtime, never
    validates credentials, and never talks to the platform API. Its job is
    to show and dismiss screens, relay their callbacks back to the
    orchestrating controller, and apply small visual tweaks like the
    update banner or connection-failed status text.
    """

    def __init__(
        self,
        *,
        flow_state: ProfileFlowState,
        state: ProfileStatePort,
        ui: ProfileUiPort,
        screen: ProfileScreenPort,
        store: ProfileStorePort,
        async_actions: ProfileAsyncActions,
    ) -> None:
        self._flow_state = flow_state
        self._state = state
        self._ui = ui
        self._screen = screen
        self._store = store
        self._async_actions = async_actions
        # Wired by :meth:`wire` once the sibling controllers are constructed.
        self._apply_profile: _ApplyProfile | None = None
        self._retry_boot: _RetryBoot | None = None

    def wire(
        self,
        *,
        apply_profile: _ApplyProfile,
        retry_boot: _RetryBoot,
    ) -> None:
        """Attach cross-controller callbacks.

        Called by :class:`ProfileManager` after all three controllers exist.
        Both callbacks are expected to indirect through the facade so that
        monkeypatching facade methods in tests still wins.
        """
        self._apply_profile = apply_profile
        self._retry_boot = retry_boot

    # ------------------------------------------------------------------
    # Profile picker dialog
    # ------------------------------------------------------------------

    def open_profile_dialog(self) -> None:
        """Open the profile picker dialog."""
        if self._screen.profile_dialog_visible():
            self._screen.hide_profile_dialog()
            return
        user_config = self._store.read_user_config()
        if not user_config.servers:
            self._ui.flash("No saved profiles. Use /login first.", severity="warning")
            return
        self._screen.show_profile_dialog(
            user_config.servers,
            self._store.active_profile_name(),
        )
        self._screen.focus_composer()

    def handle_profile_deleted(self, profile_name: str) -> None:
        """Delete a saved profile and report the result to the user."""
        if self._store.delete_profile(profile_name):
            self._ui.flash(f"Removed profile: {profile_name}", severity="info")
        else:
            self._ui.flash(f"Profile not found: {profile_name}", severity="warning")

    # ------------------------------------------------------------------
    # Auth modal lifecycle
    # ------------------------------------------------------------------

    def show_auth_modal(
        self,
        server_url: str | None = None,
        force_new_key: bool = False,
        reason: str | None = None,
    ) -> None:
        """Push the auth modal.

        Always dismisses any connection-error modal first so the user never
        sees both at once.
        """
        from dreadnode.version import VERSION

        self.dismiss_connection_error_screen()

        resolved_url = server_url or self._state.server_url()
        update_available = self._state.update_available()
        update_banner = (
            "Update available: "
            f"v{VERSION} → v{update_available} — "
            "press U to update now, or /update after login"
            if update_available
            else None
        )
        # Carry the active profile name into the modal so a re-auth flow
        # writes new credentials back to the same profile (e.g. `--profile local`)
        # instead of creating a fresh one keyed by username.
        current = self._state.current_profile()
        profile_name = current.name if current is not None else None
        self._state.set_runtime_connected(True)
        logger.debug("Screen push | screen=AuthModal url={}", resolved_url)
        self._screen.push_screen(
            AuthModal(
                resolved_url,
                force_new_key=force_new_key,
                reason=reason,
                update_banner=update_banner,
                profile_name=profile_name,
            ),
            callback=self.on_auth_complete,
        )

    def on_auth_complete(self, result: Profile | None) -> None:
        """Handle completion of the auth modal.

        If the user dismissed the modal to switch profiles, reopen the
        profile picker instead of exiting. If the modal closed with no
        result, exit the app (no credentials means nothing to do). Otherwise
        apply the returned profile via the wired ``apply_profile`` callback.
        """
        if self._flow_state.switching_profile:
            self._flow_state.switching_profile = False
            self.open_profile_dialog()
            return
        if result is None:
            self._screen.exit_app()
            return
        if self._apply_profile is None:
            logger.warning("AuthModalController: apply_profile callback not wired")
            return
        self._async_actions.run_command(self._apply_profile, result)

    def request_auth_modal_profile_switch(self) -> None:
        """Dismiss the auth modal into profile selection mode."""
        self._flow_state.switching_profile = True
        screen = self._screen.current_screen()
        if isinstance(screen, AuthModal):
            screen.dismiss(None)

    def try_update_auth_modal_banner(self, info: "UpdateInfo") -> None:
        """Push update-banner text into the mounted auth modal, if any."""
        try:
            from dreadnode.version import VERSION

            banner = (
                "Update available: "
                f"v{VERSION} → v{info.latest} — "
                "press U to update now, or /update after login"
            )
            self._screen.update_auth_banner(banner)
        except Exception:
            logger.opt(exception=True).debug("Failed to update auth modal banner")

    # ------------------------------------------------------------------
    # Connection-error modal lifecycle
    # ------------------------------------------------------------------

    def enter_connection_failed(self, message: str) -> None:
        """Show or update the connection-error modal."""
        self._ui.set_connection_status(STATUS_CONNECTION_FAILED)

        screen = self._screen.current_screen()
        if isinstance(screen, ConnectionErrorScreen):
            screen.show_error(message)
            return

        self._screen.push_screen(
            ConnectionErrorScreen(message),
            callback=self.on_connection_error_dismiss,
        )

    def dismiss_connection_error_screen(self) -> None:
        """Dismiss the connection-error screen if it is mounted."""
        screen = self._screen.current_screen()
        if isinstance(screen, ConnectionErrorScreen):
            screen.dismiss(True)

    def on_connection_error_dismiss(self, retry: bool | None) -> None:
        """Handle dismissal of the connection-error screen."""
        if self._flow_state.switching_profile:
            self._flow_state.switching_profile = False
            self.open_profile_dialog()
            return
        if retry:
            if self._retry_boot is None:
                logger.warning("AuthModalController: retry_boot callback not wired")
                return
            self._retry_boot()
        else:
            self._screen.exit_app()

    def request_connection_error_profile_switch(self) -> None:
        """Dismiss the connection-error screen into profile selection mode."""
        self._flow_state.switching_profile = True
        screen = self._screen.current_screen()
        if isinstance(screen, ConnectionErrorScreen):
            screen.dismiss(False)


# =============================================================================
# ProfileRuntimeController
# =============================================================================


class ProfileRuntimeController:
    """Owns the runtime-facing side-effects of applying a connected profile.

    Given an already-authenticated profile, this controller:

    - sets up the platform API context
    - restarts (or starts) the local runtime
    - refreshes runtime info, sessions, and skills
    - refreshes platform models and the litellm proxy key
    - creates an initial session
    - flips reactive state (authenticated, runtime_connected) to ready

    It does **not** validate credentials, open auth modals, or choose which
    profile to apply. Those concerns live in :class:`AuthModalController`
    and :class:`BootAndAuthRecoveryController`.
    """

    def __init__(
        self,
        *,
        state: ProfileStatePort,
        ui: ProfileUiPort,
        screen: ProfileScreenPort,
        runtime: ProfileRuntimePort,
        models: ProfileModelPort,
        store: ProfileStorePort,
    ) -> None:
        self._state = state
        self._ui = ui
        self._screen = screen
        self._runtime = runtime
        self._models = models
        self._store = store
        # Wired by :meth:`wire` once the sibling controllers are constructed.
        self._handle_auth_error: _HandleAuthError | None = None
        self._enter_connection_failed: _EnterConnectionFailed | None = None

    def wire(
        self,
        *,
        handle_auth_error: _HandleAuthError,
        enter_connection_failed: _EnterConnectionFailed,
    ) -> None:
        """Attach cross-controller callbacks."""
        self._handle_auth_error = handle_auth_error
        self._enter_connection_failed = enter_connection_failed

    async def apply_auth_profile(self, profile: Profile) -> bool:
        """Apply a connected profile and restart runtime state around it.

        Returns ``True`` on success, ``False`` if platform refresh failed
        with an auth error or a connection error (both of which are routed
        to the sibling controllers via wired callbacks).
        """
        self._state.set_current_profile(profile)
        self._models.clear_platform_proxy_state()
        self._state.set_model(self._models.model_from_profile(profile))

        if profile.organization and profile.workspace:
            api = ApiClient(profile.url, api_key=profile.api_key)
            self._runtime.set_api_context(api, profile.organization, profile.workspace)
        self._runtime.set_platform_profile(profile)
        self._state.set_runtime_connected(False)

        if self._runtime.local_runtime_started():
            self._ui.set_boot_status(STATUS_RESTARTING)
            await self._runtime.restart_local_runtime()
        else:
            self._ui.set_boot_status(STATUS_STARTING)
            await self._runtime.start_local_runtime()

        self._ui.set_boot_status(STATUS_LOADING_CAPABILITIES)
        await self._runtime.refresh_runtime()
        self._ui.set_boot_status(STATUS_SYNCING)
        await self._runtime.refresh_server_sessions()
        await self._runtime.refresh_skill_names()
        try:
            await self._models.refresh_platform_models_and_key(
                ApiClient(profile.url, api_key=profile.api_key)
            )
        except AuthenticationError:
            if self._handle_auth_error is not None:
                self._handle_auth_error("Session expired — please sign in again")
            return False
        except Exception as exc:
            logger.warning("Platform connection failed during profile apply: {}", exc)
            if self._enter_connection_failed is not None:
                self._enter_connection_failed(f"Unable to reach {profile.url}")
            return False

        # Login/profile-switch lands the user on a clean slate — no session
        # is created until they send their first message (or invoke /rename).
        # Eagerly creating one here used to spam the sidebar with empty
        # ``Session <timestamp>`` rows on every login.
        self._state.set_active_session_id(None)
        self._ui.sync_conversation()
        self._ui.update_context()
        self._store.set_in_memory_profile(profile.name, profile)
        self._state.set_authenticated(True)
        self._state.set_runtime_connected(True)
        self._ui.set_status(STATUS_READY, busy=False)
        self._ui.set_composer_enabled(True)
        self._screen.focus_composer()
        return True


# =============================================================================
# BootAndAuthRecoveryController
# =============================================================================


class BootAndAuthRecoveryController:
    """Owns the boot flow, credential validation, and login/logout/switch.

    This controller orchestrates :class:`AuthModalController` and
    :class:`ProfileRuntimeController` during boot and during credential
    transitions, but it does not implement auth modal UI or runtime
    side-effects itself.
    """

    def __init__(
        self,
        *,
        flow_state: ProfileFlowState,
        state: ProfileStatePort,
        ui: ProfileUiPort,
        runtime: ProfileRuntimePort,
        models: ProfileModelPort,
        store: ProfileStorePort,
        async_actions: ProfileAsyncActions,
    ) -> None:
        self._flow_state = flow_state
        self._state = state
        self._ui = ui
        self._runtime = runtime
        self._models = models
        self._store = store
        self._async_actions = async_actions
        # Wired by :meth:`wire` once the sibling controllers are constructed.
        self._show_auth_modal: _ShowAuthModal | None = None
        self._apply_auth_profile: _ApplyProfile | None = None
        self._enter_connection_failed: _EnterConnectionFailed | None = None
        self._dismiss_connection_error_screen: _DismissConnectionErrorScreen | None = None

    def wire(
        self,
        *,
        show_auth_modal: _ShowAuthModal,
        apply_auth_profile: _ApplyProfile,
        enter_connection_failed: _EnterConnectionFailed,
        dismiss_connection_error_screen: _DismissConnectionErrorScreen,
    ) -> None:
        """Attach cross-controller callbacks."""
        self._show_auth_modal = show_auth_modal
        self._apply_auth_profile = apply_auth_profile
        self._enter_connection_failed = enter_connection_failed
        self._dismiss_connection_error_screen = dismiss_connection_error_screen

    # ------------------------------------------------------------------
    # Boot
    # ------------------------------------------------------------------

    def schedule_boot(self) -> None:
        """Start the boot flow as an exclusive background worker."""
        self._async_actions.run_exclusive(
            self.boot(),
            group="boot",
        )

    async def boot(self) -> None:
        """Boot the runtime using the current active profile."""
        boot_t0 = time.monotonic()
        self._models.clear_platform_proxy_state()
        self._ui.set_boot_status(STATUS_AUTHENTICATING)
        self._state.set_authenticated(False)

        profile = self._state.current_profile()
        if not profile or not profile.api_key or not profile.organization or not profile.workspace:
            self._ui.set_connection_status(STATUS_AUTH_REQUIRED)
            self._ui.set_status(STATUS_AUTH_REQUIRED, busy=False)
            self._invoke_show_auth_modal(profile.url if profile else None)
            return

        masked = profile.api_key[:6] + "..." if len(profile.api_key) > 6 else "***"
        logger.info(
            "Boot: validating key {} against {} (org={}, workspace={})",
            masked,
            profile.url,
            profile.organization,
            profile.workspace,
        )

        api = ApiClient(profile.url, api_key=profile.api_key)
        if not await self.validate_api_key_with_retry(api, profile):
            return

        org = profile.organization
        workspace = profile.workspace

        # Kick off the local runtime boot now — it only needs the profile's
        # scalar fields (url/api_key/org/workspace/project), which are already
        # in memory. Running it concurrently with the remaining platform API
        # calls (org/workspace validation, identity hydration, user prefs +
        # LiteLLM key provisioning) collapses the critical path substantially.
        self._runtime.set_api_context(api, org, workspace)
        self._runtime.set_platform_profile(profile)
        # Each timed task records its own elapsed work time into the matching
        # list slot. Logging the wall-clock between create_task() and await
        # would conflate "task work" with "time we spent on other branches
        # before getting back to await it" — useless for spotting what's
        # actually slow.
        runtime_start_ms: list[float] = []
        platform_models_ms: list[float] = []

        async def _timed_runtime_start() -> None:
            t0 = time.monotonic()
            try:
                await self._runtime.start_local_runtime()
            finally:
                runtime_start_ms.append((time.monotonic() - t0) * 1000)

        async def _timed_platform_models() -> None:
            t0 = time.monotonic()
            try:
                await self._models.refresh_platform_models_and_key(api)
            finally:
                platform_models_ms.append((time.monotonic() - t0) * 1000)

        self._ui.set_boot_status(STATUS_STARTING)
        runtime_boot_task = asyncio.create_task(_timed_runtime_start())
        runtime_boot_task.add_done_callback(_log_background_boot_failure)

        try:
            t0 = time.monotonic()
            await asyncio.to_thread(api.get_organization, org)
            workspaces = await asyncio.to_thread(api.list_workspaces, org)
            logger.debug(
                "Boot timing | validate_org_workspace={:.0f}ms", (time.monotonic() - t0) * 1000
            )
        except Exception as exc:
            self._ui.set_connection_status(STATUS_AUTH_REQUIRED)
            self._ui.set_status(STATUS_AUTH_REQUIRED, busy=False)
            logger.warning("Boot: failed to validate org/workspace: {}", exc)
            self._invoke_show_auth_modal(
                reason="Could not verify your account — please sign in again"
            )
            # Let the runtime boot finish in the background — a subsequent
            # successful auth will restart it with fresh creds anyway.
            return

        if not any(getattr(ws, "key", None) == workspace for ws in workspaces):
            self._ui.set_connection_status(STATUS_AUTH_REQUIRED)
            self._ui.set_status(STATUS_AUTH_REQUIRED, busy=False)
            logger.warning("Boot: workspace {!r} not found in org {!r}", workspace, org)
            self._invoke_show_auth_modal(reason="Workspace not found — please sign in again")
            return

        try:
            user = await asyncio.to_thread(api.get_user)
            profile._user = user
            profile.promote_identity_to_defaults()
            if profile.name:
                self._store.save_profile(profile)
                self._store.activate_profile(profile.name)
                logger.debug("Boot: hydrated identity for profile {!r}", profile.name)
        except Exception:
            logger.opt(exception=True).debug("Boot: identity hydration failed (non-fatal)")

        resume_session_id = self._state.resume_session_id()
        # Platform models + LiteLLM provisioning can overlap with the tail of
        # the runtime boot and the subsequent runtime refreshes.
        platform_models_task = asyncio.create_task(_timed_platform_models())
        try:
            try:
                await runtime_boot_task
            except BaseException:
                platform_models_task.cancel()
                with contextlib.suppress(BaseException):
                    await platform_models_task
                raise
            if runtime_start_ms:
                logger.debug("Boot timing | runtime_start={:.0f}ms", runtime_start_ms[0])
            self._ui.set_boot_status(STATUS_LOADING_CAPABILITIES)
            t0 = time.monotonic()
            await self._runtime.refresh_runtime()
            logger.debug("Boot timing | refresh_runtime={:.0f}ms", (time.monotonic() - t0) * 1000)
            self._ui.set_boot_status(STATUS_SYNCING)
            t0 = time.monotonic()
            await self._runtime.refresh_server_sessions()
            logger.debug("Boot timing | refresh_sessions={:.0f}ms", (time.monotonic() - t0) * 1000)
            try:
                await platform_models_task
                if platform_models_ms:
                    logger.debug(
                        "Boot timing | platform_models_and_key={:.0f}ms",
                        platform_models_ms[0],
                    )
            except AuthenticationError:
                self.handle_authentication_error("Session expired — please sign in again")
                return

            if resume_session_id:
                await self._runtime.resume_requested_session()
            else:
                self._state.set_active_session_id(None)
                self._ui.sync_conversation()
                self._ui.update_context()
            self._state.set_authenticated(True)
            self._store.set_in_memory_profile(profile.name, profile)
            await self._runtime.refresh_skill_names()
            logger.info("Boot timing | total={:.0f}ms", (time.monotonic() - boot_t0) * 1000)
            self._state.set_runtime_connected(True)
            if self._dismiss_connection_error_screen is not None:
                self._dismiss_connection_error_screen()
            self._ui.set_status(STATUS_READY, busy=False)
            self._ui.set_composer_enabled(True)
            # The screen port on this controller would be the runtime
            # controller's concern; the boot controller doesn't own
            # ``focus_composer`` directly. The runtime controller handles
            # focus after its own apply path.
            initial_agent, initial_prompt, initial_policy = self._state.consume_initial_inputs()
            should_create_session = not resume_session_id and (
                initial_agent or initial_prompt or initial_policy
            )
            if should_create_session:
                if initial_agent:
                    available = {
                        "default",
                        *{agent["name"] for agent in self._runtime.collect_agents()},
                    }
                    if initial_agent not in available:
                        self._ui.flash(f"Unknown agent: {initial_agent}", severity="warning")
                        initial_agent = None
                self._ui.dismiss_welcome()
                agent_arg = (
                    None if (not initial_agent or initial_agent == "default") else initial_agent
                )
                await self._runtime.create_new_session(agent=agent_arg, policy=initial_policy)
                if initial_prompt:
                    self._runtime.send_chat(initial_prompt)
            elif resume_session_id and initial_prompt:
                self._ui.dismiss_welcome()
                self._runtime.send_chat(initial_prompt)
        except Exception as exc:
            logger.opt(exception=True).warning("Boot failed while starting runtime")
            self._state.set_authenticated(False)
            self._ui.set_connection_status(STATUS_CONNECTION_FAILED)
            self._ui.write_activity(str(exc), style="error")
            self._ui.flash(str(exc), severity="error")
            self._ui.set_status(STATUS_CONNECTION_FAILED, busy=False)
            self._ui.set_composer_enabled(False)

    async def validate_api_key_with_retry(self, api: ApiClient, profile: Profile) -> bool:
        """Validate the profile's API key with exponential backoff."""
        backoffs = [1.0, 2.0, 4.0]
        t0 = time.monotonic()
        for attempt in range(len(backoffs) + 1):
            try:
                response = await asyncio.to_thread(api._request, "GET", "/user")
            except httpx.RequestError as exc:
                logger.warning("Boot: connection attempt {} failed: {}", attempt + 1, exc)
                if attempt < len(backoffs):
                    await asyncio.sleep(backoffs[attempt])
                    continue
                logger.warning("Boot: cannot reach {} after {} attempts", profile.url, attempt + 1)
                if self._enter_connection_failed is not None:
                    self._enter_connection_failed(f"Unable to reach {profile.url}")
                return False

            if response.status_code == 401:
                self._ui.set_connection_status(STATUS_AUTH_REQUIRED)
                self._ui.set_status(STATUS_AUTH_REQUIRED, busy=False)
                logger.warning("Boot: API key rejected (401) by {}", profile.url)
                self._invoke_show_auth_modal(
                    reason="Your session has expired — please sign in again"
                )
                return False

            if response.is_success:
                logger.debug(
                    "Boot timing | validate_key={:.0f}ms",
                    (time.monotonic() - t0) * 1000,
                )
                return True

            if response.status_code >= 500 and attempt < len(backoffs):
                await asyncio.sleep(backoffs[attempt])
                continue

            logger.warning("Boot: server error ({}) from {}", response.status_code, profile.url)
            if self._enter_connection_failed is not None:
                self._enter_connection_failed(
                    f"Server error ({response.status_code}) at {profile.url}"
                )
            return False

        return False

    # ------------------------------------------------------------------
    # Profile switching + login/logout
    # ------------------------------------------------------------------

    async def switch_profile(self, profile_name: str) -> None:
        """Switch to a different saved profile."""
        config = self._store.read_user_config()
        profile = config.get(profile_name)
        if profile is None:
            self._ui.flash(f"Profile not found: {profile_name}", severity="warning")
            return

        # The auth modal controller's dismiss_pushed_screens path is routed
        # here via ``_ui`` and friends; we only need to flip reactives that
        # belong to state.
        self._state.set_authenticated(False)
        self._ui.set_composer_enabled(False)
        self._state.set_active_session_id(None)
        self._ui.sync_conversation()

        if not profile.api_key:
            self._ui.flash(
                f"Profile {profile_name} needs authentication",
                severity="warning",
            )
            self._invoke_show_auth_modal(profile.url)
            return

        self._ui.flash(
            f"Switching to {profile_name} — sessions cleared",
            severity="warning",
        )
        try:
            if self._apply_auth_profile is None:
                logger.warning("BootController: apply_auth_profile callback not wired")
                return
            applied = await self._apply_auth_profile(profile)
        except AuthenticationError:
            self.handle_authentication_error("Session expired — please sign in again")
            return
        except Exception as exc:
            logger.warning("Profile switch to {} failed: {}", profile_name, exc)
            if self._enter_connection_failed is not None:
                self._enter_connection_failed(f"Unable to reach {profile.url}")
            return
        if not applied:
            return

        self._store.activate_profile(profile_name)

    async def login_command(self, args: list[str] | None = None) -> None:
        """Log in with an API key, or open the auth modal when no key is supplied."""
        self._ui.set_status(STATUS_LOGGING_IN, busy=True)
        try:
            server_url, api_key = _parse_login_args(
                args or [],
                default_platform_url=self._state.server_url(),
            )
        except ValueError as exc:
            self._ui.flash(str(exc), severity="warning")
            self._ui.set_status(STATUS_READY, busy=False)
            return
        if api_key is None:
            self._ui.set_connection_status(STATUS_AUTH_REQUIRED)
            self._ui.set_status(STATUS_AUTH_REQUIRED, busy=False)
            self._invoke_show_auth_modal(server_url)
            return

        try:
            profile = await asyncio.to_thread(_login_with_api_key, server_url, api_key)
        except Exception as exc:
            self._ui.set_connection_status(STATUS_AUTH_REQUIRED)
            self._ui.set_status(STATUS_AUTH_REQUIRED, busy=False)
            logger.warning("Login failed: {}", exc)
            self._invoke_show_auth_modal(server_url, reason="Login failed — please try again")
            return
        self._ui.flash(
            "Restarting runtime to apply platform authentication",
            severity="warning",
        )
        if self._apply_auth_profile is None:
            logger.warning("BootController: apply_auth_profile callback not wired")
            return
        await self._apply_auth_profile(profile)

    async def logout_command(self) -> None:
        """Log out the active profile and restart runtime without platform sync."""
        logout_server_url = self._state.server_url()
        try:
            _name, profile = self._store.active_profile()
        except Exception:
            profile = None
            logger.opt(exception=True).warning(
                "Failed to read active profile for API key revocation"
            )
        if profile and profile.api_key and profile.url:
            try:
                api = ApiClient(profile.url, api_key=profile.api_key)
                await asyncio.to_thread(api.revoke_self_api_key)
            except Exception:
                logger.opt(exception=True).warning("Failed to revoke API key during logout")
        disconnected: str | None = None
        try:
            disconnected = self._store.disconnect_profile()
        except Exception as exc:
            self._ui.flash(f"Failed to disconnect profile: {exc}", severity="warning")
        if disconnected:
            self._ui.flash(
                f"Logged out from {disconnected}; credentials revoked",
                severity="warning",
            )
        else:
            self._ui.flash(
                "No saved profile found; restarting runtime without platform sync",
                severity="warning",
            )
        self._runtime.clear_platform_profile()
        self._models.clear_platform_proxy_state()
        self._store.clear_in_memory_profile()
        self._state.set_authenticated(False)

        if self._runtime.local_runtime_started():
            self._state.set_runtime_connected(False)
            self._ui.set_boot_status(STATUS_RESTARTING)
            await self._runtime.restart_local_runtime()
            self._ui.set_boot_status(STATUS_LOADING_CAPABILITIES)
            await self._runtime.refresh_runtime()
            self._ui.set_boot_status(STATUS_SYNCING)
            await self._runtime.refresh_server_sessions()
            await self._runtime.refresh_skill_names()
            if self._state.active_session_id() is None:
                await self._runtime.create_new_session()
        self._ui.set_status(STATUS_READY, busy=False)
        self._invoke_show_auth_modal(logout_server_url, force_new_key=True)

    # ------------------------------------------------------------------
    # Auth error recovery
    # ------------------------------------------------------------------

    def handle_authentication_error(self, message: str) -> None:
        """Reset auth state and enter the auth modal."""
        logger.warning("Auth error triggered: {}", message)
        self._state.set_authenticated(False)
        self._models.clear_platform_proxy_state()
        self._invoke_show_auth_modal(self._state.server_url(), reason=message)

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------

    def _invoke_show_auth_modal(
        self,
        server_url: str | None = None,
        force_new_key: bool = False,
        reason: str | None = None,
    ) -> None:
        """Route an auth-modal request through the wired callback."""
        if self._show_auth_modal is None:
            logger.warning("BootController: show_auth_modal callback not wired")
            return
        # Explicit keyword call so test patches that inspect *args/**kwargs
        # see the same shape as the facade method.
        if reason is None and not force_new_key:
            self._show_auth_modal(server_url)
            return
        if reason is None:
            self._show_auth_modal(server_url, force_new_key=force_new_key)
            return
        self._show_auth_modal(server_url, reason=reason)


# =============================================================================
# ProfileManager facade
# =============================================================================


class ProfileManager:
    """Composition facade over the three profile controllers.

    Constructs :class:`AuthModalController`, :class:`ProfileRuntimeController`,
    and :class:`BootAndAuthRecoveryController`, wires their cross-dependencies,
    and delegates every public method to the owning controller. App code and
    existing tests continue to call this class through the same surface as
    before the split — the behavior now lives in three testable units with
    clearly scoped responsibilities.

    Cross-controller callbacks are wired through lambdas that look up the
    facade's method at *call time*. That preserves existing tests which
    patch methods on the manager instance:

    .. code-block:: python

        manager.show_auth_modal = lambda *args, **kwargs: ...
        await manager.boot()  # still hits the patched version from inside
                              # the boot controller
    """

    def __init__(
        self,
        *,
        flow_state: ProfileFlowState,
        state: ProfileStatePort,
        ui: ProfileUiPort,
        screen: ProfileScreenPort,
        runtime: ProfileRuntimePort,
        models: ProfileModelPort,
        store: ProfileStorePort,
        async_actions: ProfileAsyncActions,
    ) -> None:
        self._flow_state = flow_state
        self._state = state
        self._ui = ui
        self._screen = screen
        self._runtime = runtime
        self._models = models
        self._store = store
        self._async_actions = async_actions

        self._auth = AuthModalController(
            flow_state=flow_state,
            state=state,
            ui=ui,
            screen=screen,
            store=store,
            async_actions=async_actions,
        )
        self._runtime_ctrl = ProfileRuntimeController(
            state=state,
            ui=ui,
            screen=screen,
            runtime=runtime,
            models=models,
            store=store,
        )
        self._boot = BootAndAuthRecoveryController(
            flow_state=flow_state,
            state=state,
            ui=ui,
            runtime=runtime,
            models=models,
            store=store,
            async_actions=async_actions,
        )

        # Wire cross-controller callbacks with lambdas that indirect through
        # the facade so that tests which patch ``self.show_auth_modal``,
        # ``self.apply_auth_profile``, etc. see their patched versions from
        # inside the sub-controllers.
        self._auth.wire(
            apply_profile=lambda profile: self.apply_auth_profile(profile),
            retry_boot=lambda: self.schedule_boot(),
        )
        self._runtime_ctrl.wire(
            handle_auth_error=lambda message: self.handle_authentication_error(message),
            enter_connection_failed=lambda message: self.enter_connection_failed(message),
        )
        self._boot.wire(
            show_auth_modal=lambda *args, **kwargs: self.show_auth_modal(*args, **kwargs),
            apply_auth_profile=lambda profile: self.apply_auth_profile(profile),
            enter_connection_failed=lambda message: self.enter_connection_failed(message),
            dismiss_connection_error_screen=lambda: self.dismiss_connection_error_screen(),
        )

    # ------------------------------------------------------------------
    # Delegations — AuthModalController
    # ------------------------------------------------------------------

    def open_profile_dialog(self) -> None:
        self._auth.open_profile_dialog()

    def handle_profile_deleted(self, profile_name: str) -> None:
        self._auth.handle_profile_deleted(profile_name)

    def show_auth_modal(
        self,
        server_url: str | None = None,
        force_new_key: bool = False,
        reason: str | None = None,
    ) -> None:
        self._auth.show_auth_modal(server_url, force_new_key=force_new_key, reason=reason)

    def on_auth_complete(self, result: Profile | None) -> None:
        self._auth.on_auth_complete(result)

    def request_auth_modal_profile_switch(self) -> None:
        self._auth.request_auth_modal_profile_switch()

    def try_update_auth_modal_banner(self, info: "UpdateInfo") -> None:
        self._auth.try_update_auth_modal_banner(info)

    def enter_connection_failed(self, message: str) -> None:
        self._auth.enter_connection_failed(message)

    def dismiss_connection_error_screen(self) -> None:
        self._auth.dismiss_connection_error_screen()

    def on_connection_error_dismiss(self, retry: bool | None) -> None:
        self._auth.on_connection_error_dismiss(retry)

    def request_connection_error_profile_switch(self) -> None:
        self._auth.request_connection_error_profile_switch()

    # ------------------------------------------------------------------
    # Delegations — ProfileRuntimeController
    # ------------------------------------------------------------------

    async def apply_auth_profile(self, profile: Profile) -> bool:
        return await self._runtime_ctrl.apply_auth_profile(profile)

    # ------------------------------------------------------------------
    # Delegations — BootAndAuthRecoveryController
    # ------------------------------------------------------------------

    def schedule_boot(self) -> None:
        self._boot.schedule_boot()

    async def boot(self) -> None:
        await self._boot.boot()

    async def validate_api_key_with_retry(self, api: ApiClient, profile: Profile) -> bool:
        return await self._boot.validate_api_key_with_retry(api, profile)

    async def switch_profile(self, profile_name: str) -> None:
        await self._boot.switch_profile(profile_name)

    async def login_command(self, args: list[str] | None = None) -> None:
        await self._boot.login_command(args)

    async def logout_command(self) -> None:
        await self._boot.logout_command()

    def handle_authentication_error(self, message: str) -> None:
        self._boot.handle_authentication_error(message)
