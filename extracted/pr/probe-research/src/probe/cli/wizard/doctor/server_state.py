"""the server's half of the snapshot: the login check from the wizard's device-state answer, or the old /v1/me way."""

from __future__ import annotations

import dataclasses
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from probe.cli.wizard.state.state import Capabilities
from probe.cli.wizard.state.device_state import DeviceState


def name_account() -> str | None:
    """The signed-in account's email, asked the old way (`/v1/me` over the SDK
    client: its own timeout, the environment's proxies), or None.

    For the one decision that must not go on a guess: redeeming an install code
    switches the device's account irreversibly, and is confirmed only when the
    account being replaced can be named. When the wizard's one call could not
    name it -- a slow server, a network it could not cross -- ask this way."""
    try:
        from probe.sdk.settings.settings import resolve

        settings = resolve()
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None
    return _check_login(settings).logged_in_as or None


@dataclass(frozen=True)
class _LoginCheck:
    logged_in_as: str | None = None
    #: True accepted, False refused (the wizard's sign-in trigger), None unknown.
    api_credential_valid: bool | None = None
    warnings: tuple[str, ...] = ()


def _check_login(settings) -> _LoginCheck:
    """The old way: `/v1/me`, with the SDK client."""
    if not settings.token:
        return _LoginCheck()
    try:
        from probe.sdk.client.client import Client
        from probe.foundation.request_identity.surface import Surface

        with Client(settings=settings, async_writes=False, surface=Surface.CLI.value) as client:
            email = str(client.me().get("email") or "")
            return _LoginCheck(logged_in_as=email, api_credential_valid=True)
    except Exception as exc:  # noqa: BLE001
        from probe.sdk.errors import AuthError, ScopeError

        return _LoginCheck(
            api_credential_valid=False if isinstance(exc, (AuthError, ScopeError)) else None,
            warnings=(
                (f"could not verify login against {settings.base_url}: {exc}",)
                if settings.base_url
                else ()
            ),
        )


def _login_from_state(state: DeviceState, *, has_token: bool, base_url: str | None) -> _LoginCheck:
    """The login half of the wizard's one call, in `_check_login`'s shape."""
    if not has_token:
        return _LoginCheck()
    if state.answered and state.account_valid:
        return _LoginCheck(logged_in_as=state.account_email or "", api_credential_valid=True)
    if state.answered and state.account_valid is False:
        reason = "the server refused this credential"
    elif state.answered:
        reason = "the server could not check it"
    else:
        reason = state.error or "no answer"
    return _LoginCheck(
        api_credential_valid=False if state.answered and state.account_valid is False else None,
        warnings=(f"could not verify login against {base_url}: {reason}",) if base_url else (),
    )


def with_server_state(
    caps: Capabilities, state: DeviceState, *, has_token: bool, base_url: str | None
) -> Capabilities:
    """`caps` with the server's half read from `state`: the half `collect`
    reads through `device_state_scope`, for a caller that asked the server ONCE
    for every agent after their own checks (`probe status --refresh`). Nothing
    is asked here, so `state` carries a verdict for every agent with a capture
    credential, or says nothing is known (UNREACHABLE)."""
    login = _login_from_state(state, has_token=has_token, base_url=base_url)
    return dataclasses.replace(
        caps,
        logged_in_as=login.logged_in_as or None,
        api_credential_valid=login.api_credential_valid,
        capture_credential_valid=(
            state.capture.get(caps.agent_source) if caps.capture_token_sources else None
        ),
    )


#: The wizard's ONE server call for the `collect()` running in this context
#: (`capabilities.fetch_device_state`), as a zero-argument resolver -- usually
#: a pending future's bounded `result`. Scoped like the wizard scopes the agent
#: (`PROBE_AGENT`), so `collect()` keeps one signature for every caller.
_remote_state: ContextVar[Callable[[], DeviceState] | None] = ContextVar(
    "probe_wizard_device_state", default=None
)


@contextmanager
def device_state_scope(remote: Callable[[], DeviceState]) -> Iterator[None]:
    """Have `collect()` read the server's state from `remote` in this block."""
    token = _remote_state.set(remote)
    try:
        yield
    finally:
        _remote_state.reset(token)
