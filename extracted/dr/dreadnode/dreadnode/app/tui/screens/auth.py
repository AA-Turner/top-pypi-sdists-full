"""Authentication modal screen for the Dreadnode TUI."""

from __future__ import annotations

import asyncio
import secrets
import time
import typing as t
import webbrowser
from datetime import UTC, datetime

from rich.markup import escape
from rich.text import Text
from textual import on, work
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from dreadnode.app.api.client import ApiClient
from dreadnode.app.config import Profile, UserConfig, resolve_default_workspace, urls_match
from dreadnode.app.tui.auth_flow import (
    _active_profile,
    _save_profile,
)
from dreadnode.app.tui.theme import (
    BRAND,
    FG_SUBTLE,
    pick_logo,
)

if t.TYPE_CHECKING:
    from textual.app import ComposeResult

_POLL_INTERVAL = 2.0
_POLL_FAILURE_LIMIT = 3
_EXPIRY_BUFFER = 10.0


class _AuthBanner(Static):
    """Responsive logo banner — biggest variant that fits, falls back to plain text."""

    def render(self) -> Text:
        t = Text(justify="center")
        w = self.size.width
        logo = pick_logo(w)
        if logo is not None:
            for line in logo.splitlines():
                t.append(line, style=BRAND)
                t.append("\n")
        else:
            t.append("DREADNODE", style=f"bold {BRAND}")
            t.append("\n")
        return t


class _MessageAlreadyShownError(RuntimeError):
    """The modal has already rendered a fuller message than this exception carries.

    Callers must not overwrite the widget: the on-screen text may hold a key
    the exception deliberately omits, and it is the user's only copy.
    """


def _new_device_login_api_key_name() -> str:
    return f"dreadnode-{secrets.token_hex(3)}"


class AuthModal(ModalScreen[Profile | None]):
    """Full-screen auth modal — blocks all TUI interaction until authenticated."""

    class ProfileSwitchRequested(Message):
        """Posted when the user presses *p* to switch profiles."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "escape", "Back / Cancel", show=False, priority=True),
        Binding("ctrl+q", "cancel", "Cancel", show=False),
        Binding("u", "run_update", "Update", show=False),
        Binding("up", "move_selection(-1)", "Up", show=False),
        Binding("down", "move_selection(1)", "Down", show=False),
        Binding("enter", "confirm", "Confirm", show=False),
        Binding("1", "select_method(0)", "Browser", show=False),
        Binding("2", "select_method(1)", "API key", show=False),
        Binding("p", "switch_profile", "Profiles", show=False),
        Binding("r", "retry", "Retry", show=False),
    ]

    def __init__(
        self,
        server_url: str,
        force_new_key: bool = False,
        reason: str | None = None,
        update_banner: str | None = None,
        profile_name: str | None = None,
    ) -> None:
        super().__init__()
        self._server_url = server_url.rstrip("/")
        self._force_new_key = force_new_key
        self._reason = reason
        self._update_banner = update_banner
        self._profile_name = profile_name

        self._device_status = ""
        self._device_error: str | None = None
        self._api_key_error: str | None = None
        self._api_key_status: str | None = None
        self._user_code = ""
        self._verification_url = ""
        self._active_view: t.Literal["method", "device", "api_key"] = "method"
        self._selected_method_index = 0
        self._methods: list[tuple[str, str]] = [
            (
                "Browser login",
                "Opens your browser for device code authentication",
            ),
            (
                "API key",
                "Paste your Dreadnode API key directly",
            ),
        ]

        self._to_thread = asyncio.to_thread
        self._sleep = asyncio.sleep
        self._now = time.monotonic
        self._open_browser = webbrowser.open

    def compose(self) -> ComposeResult:
        with Vertical(id="auth-modal"):
            yield _AuthBanner(id="auth-banner")
            # Widgets carrying error text or server-supplied values opt out of
            # markup. Left as markup, a bracketed fragment either aborts the
            # render (Pydantic's "[type=missing, ...]") or silently vanishes
            # (a redaction placeholder) and the user sees nothing at all.
            yield Static("", id="auth-reason", markup=False)
            yield Static("", id="auth-update-banner")
            with Container(id="auth-form-wrapper"), Vertical(id="auth-content"):
                yield Static(
                    "Dreadnode can be used with your browser or by entering an API key directly.",
                    id="auth-intro",
                )
                with Vertical(id="auth-methods"):
                    yield Static("Select login method:", id="auth-method-prompt")
                    yield OptionList(id="auth-method-list")
                    yield Static(
                        "Use Up/Down to move, Enter/click/1/2 to select",
                        id="auth-method-help",
                    )
                with Vertical(id="auth-device", classes="-hidden"):
                    yield Static(
                        "Waiting for browser authorization...",
                        id="auth-status",
                        markup=False,
                    )
                    yield Static("", id="auth-user-code")
                    yield Static("", id="auth-verification-url")
                    yield Static("", id="auth-device-help")
                    yield Static("", id="auth-error", markup=False)
                with Vertical(id="auth-key", classes="-hidden"):
                    yield Static("Paste your API key:", id="auth-key-title")
                    with Horizontal(id="auth-key-bar"):
                        yield Static(">", id="auth-key-chevron")
                        yield Input(placeholder="dn_...", id="auth-api-key", password=True)
                    yield Static(
                        "Enter to submit, Esc to go back",
                        id="auth-key-help",
                    )
                    yield Static("", id="auth-key-status", markup=False)
                    yield Static("", id="auth-key-error", markup=False)

    def on_mount(self) -> None:
        if self._reason:
            self.query_one("#auth-reason", Static).update(self._reason)
        if self._update_banner:
            self.query_one("#auth-update-banner", Static).update(
                f"[bold yellow]{self._update_banner}[/]"
            )
        self._render_method_options()
        if len(UserConfig.read().servers) > 1:
            self.query_one("#auth-method-help", Static).update(
                "Use Up/Down to move, Enter/click/1/2 to select · p profiles"
            )
        self.query_one("#auth-method-list", OptionList).focus()

    def action_cancel(self) -> None:
        self._cancel_auth_workers()
        self.dismiss(None)

    def action_run_update(self) -> None:
        handler = getattr(self.app, "action_run_update", None)
        if callable(handler):
            handler()

    def action_escape(self) -> None:
        if self._active_view == "method":
            self.action_cancel()
        else:
            self._cancel_auth_workers()
            self._show_method_view()

    def action_move_selection(self, direction: int) -> None:
        if self._active_view != "method":
            return
        self._selected_method_index = max(
            0,
            min(self._selected_method_index + direction, len(self._methods) - 1),
        )
        self._render_method_options()

    def action_confirm(self) -> None:
        if self._active_view == "method":
            self._select_method(self._selected_method_index)
            return
        if self._active_view == "api_key":
            self._submit_api_key_from_input()

    def action_select_method(self, index: int) -> None:
        if self._active_view != "method":
            return
        if not 0 <= index < len(self._methods):
            return
        self._selected_method_index = index
        self._render_method_options()
        self._select_method(index)

    def action_switch_profile(self) -> None:
        if self._active_view != "method":
            return
        if len(UserConfig.read().servers) <= 1:
            return
        self.post_message(self.ProfileSwitchRequested())

    def action_retry(self) -> None:
        if self._active_view != "device":
            return
        self._begin_device_code_flow()

    @on(Input.Submitted, "#auth-api-key")
    def _on_api_key_submitted(self) -> None:
        self._submit_api_key_from_input()

    def _submit_api_key_from_input(self) -> None:
        input_widget = self.query_one("#auth-api-key", Input)
        api_key = input_widget.value.strip()
        if not api_key:
            self._set_api_key_error("API key is required.")
            return
        # The field is masked, so without this the screen is unchanged after
        # Enter and there is nothing to distinguish "working" from "ignored".
        # Users re-submit, and each press starts another auth worker.
        self._set_api_key_error("")
        self._set_api_key_status("Verifying API key...")
        self._submit_api_key(api_key)

    def _render_method_options(self) -> None:
        option_list = self.query_one("#auth-method-list", OptionList)
        option_list.clear_options()
        for index, (title, description) in enumerate(self._methods):
            label = Text()
            label.append(f"{index + 1}. ")
            label.append(title, style="bold")
            label.append(" · ", style=FG_SUBTLE)
            label.append(description, style=FG_SUBTLE)
            option_list.add_option(Option(label, id=str(index)))
        option_list.highlighted = self._selected_method_index

    def _show_method_view(self) -> None:
        self._active_view = "method"
        self.query_one("#auth-device", Vertical).add_class("-hidden")
        self.query_one("#auth-key", Vertical).add_class("-hidden")
        self.query_one("#auth-methods", Vertical).remove_class("-hidden")
        self._render_method_options()
        self.query_one("#auth-method-list", OptionList).focus()

    def _show_api_key_view(self) -> None:
        self._active_view = "api_key"
        self.query_one("#auth-methods", Vertical).add_class("-hidden")
        self.query_one("#auth-device", Vertical).add_class("-hidden")
        self.query_one("#auth-key", Vertical).remove_class("-hidden")
        self._set_api_key_error("")
        self._set_api_key_status("")
        self.query_one("#auth-api-key", Input).focus()

    def _select_method(self, index: int) -> None:
        if index == 0:
            self._show_device_view()
            self._begin_device_code_flow()
            return
        self._show_api_key_view()

    @on(OptionList.OptionSelected, "#auth-method-list")
    def _on_method_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option.id is None:
            return
        try:
            index = int(event.option.id)
        except ValueError:
            return
        self._selected_method_index = index
        self._select_method(index)

    def _show_device_view(self) -> None:
        self._active_view = "device"
        self.query_one("#auth-methods", Vertical).add_class("-hidden")
        self.query_one("#auth-key", Vertical).add_class("-hidden")
        self.query_one("#auth-device", Vertical).remove_class("-hidden")
        self.query_one("#auth-device-help", Static).update("r to retry, Esc to go back")
        self._set_device_error("")

    def _begin_device_code_flow(self) -> None:
        self._cancel_auth_workers()
        self._start_device_code_flow()

    def _cancel_auth_workers(self) -> None:
        self.workers.cancel_group(self, "auth")

    def _set_device_status(self, message: str) -> None:
        self._device_status = message
        if self.is_mounted:
            self.query_one("#auth-status", Static).update(message)

    def _set_device_error(self, message: str) -> None:
        self._device_error = message or None
        if self.is_mounted:
            self.query_one("#auth-error", Static).update(message)

    def _set_api_key_error(self, message: str) -> None:
        self._api_key_error = message or None
        if message:
            self._set_api_key_status("")
        if self.is_mounted:
            self.query_one("#auth-key-error", Static).update(message)

    def _set_api_key_status(self, message: str) -> None:
        self._api_key_status = message or None
        if self.is_mounted:
            self.query_one("#auth-key-status", Static).update(message)

    def _set_device_code_display(self, user_code: str, verification_url: str) -> None:
        self._user_code = user_code
        self._verification_url = verification_url
        if self.is_mounted:
            # These keep markup for their styling, so the server-supplied
            # values have to be escaped or a stray bracket aborts the render.
            self.query_one("#auth-user-code", Static).update(f"[bold]{escape(user_code)}[/]")
            self.query_one("#auth-verification-url", Static).update(
                f"[dim]{escape(verification_url)}[/]"
            )

    @work(exit_on_error=False, group="auth")
    async def _start_device_code_flow(self) -> None:
        profile = await self._run_device_code_flow()
        if profile is not None:
            self.dismiss(profile)

    # Exclusive: a second Enter supersedes the first attempt rather than
    # running alongside it. Concurrent attempts each write the profile, and
    # that write truncates the config file in place.
    @work(exit_on_error=False, group="auth", exclusive=True)
    async def _submit_api_key(self, api_key: str) -> None:
        try:
            profile = await self._authenticate_with_api_key(api_key)
        except _MessageAlreadyShownError:
            # The screen already holds a fuller message than this exception
            # carries; overwriting it drops the part that tells the user what
            # happened to their key.
            return
        except Exception as exc:
            # Some exceptions render as an empty string; without a fallback the
            # screen reverts to its pre-Enter state and the user cannot tell a
            # failure from a dropped keypress.
            self._set_api_key_error(str(exc) or type(exc).__name__)
            return
        # Deliberately not a `finally`: cancellation runs it too, and a
        # superseding attempt has already written its own status by then --
        # blanking it leaves auth in flight with nothing on screen.
        self._set_api_key_status("")
        self.dismiss(profile)

    def on_unmount(self) -> None:
        self._cancel_auth_workers()

    async def _run_device_code_flow(self) -> Profile | None:
        self._set_device_error("")
        while True:
            api = ApiClient(self._server_url)
            payload = await self._create_device_code(api)
            if payload is None:
                return None

            expiry_time = self._expiry_time(payload)
            device_code = payload.get("device_code")
            if not isinstance(device_code, str) or not device_code:
                self._set_device_error("Invalid device code response.")
                return None

            status, user_id = await self._poll_device_code(api, device_code, expiry_time)
            if status == "success" and user_id:
                return await self._complete_device_code_auth(api, device_code, user_id)
            if status == "expired":
                self._set_device_status("Code expired — retrying")
                continue
            return None

    async def _create_device_code(self, api: ApiClient) -> dict[str, t.Any] | None:
        self._set_device_status("Requesting device code...")
        try:
            payload = await self._to_thread(api.create_device_code)
        except Exception as exc:
            self._set_device_error(str(exc) or type(exc).__name__)
            return None

        user_code = t.cast("str | None", payload.get("user_code"))
        if not user_code:
            self._set_device_error("Device code response missing user code.")
            return None

        verification_url = f"{self._server_url}/login/device?code={user_code}"
        self._set_device_code_display(user_code, verification_url)
        self._set_device_status("Waiting for browser authorization...")

        try:
            opened = await self._to_thread(self._open_browser, verification_url)
        except Exception:
            opened = False
        if not opened:
            self._set_device_status("Open the URL below in your browser to continue.")
        return payload

    def _expiry_time(self, payload: dict[str, t.Any]) -> float:
        now = self._now()
        expires_in = payload.get("expires_in")
        if isinstance(expires_in, (int, float)):
            return now + float(expires_in)

        expires_at = payload.get("expires_at")
        if isinstance(expires_at, str):
            try:
                parsed = datetime.fromisoformat(expires_at)
                delta = (parsed - datetime.now(UTC)).total_seconds()
                return now + max(0.0, delta)
            except ValueError:
                return now
        return now

    async def _poll_device_code(
        self, api: ApiClient, device_code: str, expiry_time: float
    ) -> tuple[str, str | None]:
        consecutive_failures = 0
        while True:
            if self._now() >= (expiry_time - _EXPIRY_BUFFER):
                return "expired", None

            try:
                status_code, payload = await self._to_thread(api.poll_device_code, device_code)
            except Exception as exc:
                consecutive_failures += 1
                if consecutive_failures >= _POLL_FAILURE_LIMIT:
                    self._set_device_error(f"Polling failed: {exc}")
                    return "error", None
                await self._sleep(_POLL_INTERVAL)
                continue

            if status_code >= 500:
                consecutive_failures += 1
                if consecutive_failures >= _POLL_FAILURE_LIMIT:
                    self._set_device_error("Polling failed. Please retry.")
                    return "error", None
                await self._sleep(_POLL_INTERVAL)
                continue

            consecutive_failures = 0
            if payload and payload.get("user_id"):
                return "success", t.cast("str", payload.get("user_id"))

            await self._sleep(_POLL_INTERVAL)

    async def _complete_device_code_auth(
        self, api: ApiClient, device_code: str, user_id: str
    ) -> Profile | None:
        tokens = await self._to_thread(api.exchange_device_code, device_code)
        access_token = t.cast("str | None", tokens.get("access_token"))
        if not access_token:
            self._set_device_error("Device code exchange failed.")
            return None

        cached_api_key, cached_user = await self._resolve_cached_key(user_id)
        if cached_api_key is not None and cached_user is not None:
            try:
                return await self._build_profile(cached_api_key, cached_user, error_target="device")
            except _MessageAlreadyShownError:
                return None
            except Exception as exc:
                self._set_device_error(str(exc) or type(exc).__name__)
                return None

        try:
            created = await self._to_thread(
                api.create_api_key_with_jwt,
                access_token,
                _new_device_login_api_key_name(),
                allow_self_revoke=True,
            )
        except Exception as exc:
            self._set_device_error(f"Failed to create API key: {exc}")
            return None
        api_key = t.cast("str | None", created.get("key") or created.get("api_key"))
        if not api_key:
            self._set_device_error("Failed to mint API key.")
            return None

        user = await self._fetch_user(api_key)
        if user is None:
            self._set_device_error("Failed to validate API key.")
            return None
        try:
            return await self._build_profile(api_key, user, error_target="device")
        except _MessageAlreadyShownError:
            return None
        except Exception as exc:
            self._set_device_error(str(exc) or type(exc).__name__)
            return None

    async def _resolve_cached_key(self, user_id: str) -> tuple[str | None, t.Any | None]:
        if self._force_new_key:
            return None, None
        profile_name, profile = _active_profile()
        if profile_name is None or profile is None or not profile.api_key:
            return None, None
        if not urls_match(profile.url, self._server_url):
            return None, None
        cached_api = ApiClient(self._server_url, api_key=profile.api_key)
        try:
            user = await self._to_thread(cached_api.get_user)
        except Exception:
            return None, None
        if getattr(user, "id", None) != user_id:
            return None, None
        return profile.api_key, user

    async def _fetch_user(self, api_key: str) -> t.Any | None:
        api = ApiClient(self._server_url, api_key=api_key)
        try:
            return await self._to_thread(api.get_user)
        except Exception:
            return None

    async def _build_profile(
        self,
        api_key: str,
        user: t.Any,
        *,
        error_target: t.Literal["device", "api_key"] = "device",
    ) -> Profile:
        api = ApiClient(self._server_url, api_key=api_key)
        orgs = await self._to_thread(api.list_user_organizations)
        if not orgs:
            raise RuntimeError(
                f"No organizations found. Complete onboarding at {self._server_url} "
                "in your browser, then sign in again."
            )

        default_org = orgs[0].key
        default_ws = await self._to_thread(resolve_default_workspace, api, default_org)
        default_workspace = default_ws.key
        default_project = await self._to_thread(
            api.get_default_project_key, default_org, default_workspace
        )

        # Re-authenticate back into the named profile when one was supplied
        # (e.g. via `--profile local`); otherwise key the profile by username.
        target_name = self._profile_name or user.username

        # Check for existing profile to preserve customizations (e.g. default_model)
        from dreadnode.app.config import UserConfig

        user_config = UserConfig.read()
        existing = user_config.servers.get(target_name)
        if existing and urls_match(existing.url, self._server_url):
            existing.api_key = api_key
            existing.email = user.email_address
            existing.username = user.username
            existing.user_key = user.username
            existing.default_organization = default_org
            existing.default_workspace = default_workspace
            existing.default_project = default_project
            profile = existing
        else:
            profile = Profile(
                url=self._server_url,
                user_key=user.username,
                email=user.email_address,
                username=user.username,
                api_key=api_key,
                default_organization=default_org,
                default_workspace=default_workspace,
                default_project=default_project,
            )

        try:
            return await self._to_thread(_save_profile, target_name, profile)
        except Exception as exc:
            # The key is only worth showing when the user cannot recover it
            # any other way: the device flow mints it server-side and nothing
            # has persisted it yet. Someone who pasted their own key already
            # has it, so showing it there is pure exposure -- it renders on
            # screen and is captured by any screenshot or terminal scrollback.
            message = f"Profile save failed: {exc}."
            if error_target == "api_key":
                self._set_api_key_error(f"{message} Your API key was not saved.")
            else:
                self._set_device_error(f"{message} Please copy your API key: {api_key}")
            # Never carries the key: this propagates into logs and test output.
            # Marked so callers leave the on-screen message alone -- theirs is
            # the key-less one, and overwriting loses the only copy the user
            # will ever see of a key the platform minted server-side.
            raise _MessageAlreadyShownError(message) from exc

    async def _authenticate_with_api_key(self, api_key: str) -> Profile:
        api = ApiClient(self._server_url, api_key=api_key)
        user = await self._to_thread(api.get_user)
        return await self._build_profile(api_key, user, error_target="api_key")
