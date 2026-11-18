"""Hugging Face: one read connection per user, kept by Dreamscale, for private repos.

`dreamscale integrations hugging-face setup` opens the dashboard to sign in with Hugging Face
(its OAuth consent screen, read-only; DSL-445) and waits until the connection shows up, where
the control plane has an OAuth app and the CLI knows its dashboard. Otherwise, or with
--token / --paste, it takes a read token and sends it to the control plane, which checks it
with Hugging Face, refuses one that can write and keeps it (encrypted) for your account. The
dashboard's Integrations page shows and changes the same connection. Deployments (inspect,
create) and training then read your private repos with it. `status` shows the connection;
`remove` deletes it.

A request's own token wins: --hf-token, then HF_TOKEN. Without either the SDK sends none and
the control plane uses the connected one.
"""

from __future__ import annotations

import asyncio
import getpass
import os
import sys
import time
import webbrowser
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from dreamscale import errors
from dreamscale.config import dashboard_url, load_config, save_config
from dreamscale.control import ControlPlaneClient

NAME = "hugging-face"
NEW_TOKEN_URL = "https://huggingface.co/settings/tokens/new?tokenType=read"
SETUP_COMMAND = "dreamscale integrations hugging-face setup"
# The dashboard route that starts Hugging Face's consent flow, and where it comes back to.
CONNECT_PATH = (
    "/api/integrations/hugging-face/connect?return=/dashboard/settings/integrations"
)
WAIT_S = 300.0
POLL_S = 2.0
_MAKE_ONE = f"create a token with the Read role at {NEW_TOKEN_URL} and rerun `{SETUP_COMMAND}`"
# The control plane's refusals of a token, with the CLI's own next step.
_TOKEN_REFUSALS = {
    "hf_token_rejected": (
        "Hugging Face rejected that token", "it was mistyped, revoked or expired",
    ),
    "hf_token_can_write": (
        "that token can write to Hugging Face",
        "Dreamscale only reads your repos, so it keeps no token that can change them",
    ),
}


def _error(code, problem, cause, fix):
    return errors.DreamscaleError(errors.ErrorInfo(code, problem, cause, fix))


def token(explicit: str | None = None) -> str | None:
    """A request's own token: --hf-token, then HF_TOKEN. None lets the control plane use the
    connected account's."""
    return explicit or os.environ.get("HF_TOKEN") or None


def _call(client_factory: Callable[..., Any] | None, method: str, *args) -> dict[str, Any]:
    factory = client_factory or ControlPlaneClient
    config = load_config()
    if not config.api_key:
        raise errors.catalog("not_configured")

    async def run() -> dict[str, Any]:
        client = factory(config.control_plane_url, config.api_key)
        try:
            return await getattr(client, method)(*args)
        finally:
            await client.close()

    return asyncio.run(run())


def _forget_local_token() -> None:
    """Drop the token older SDKs saved in config.toml: the connected one replaces it."""
    config = load_config()
    if config.integrations.pop(NAME, None) is not None:
        save_config(config)


def _refusal(error: errors.DreamscaleError) -> errors.DreamscaleError:
    """The server's refusal of a token, with the command to rerun as its fix."""
    if error.code not in _TOKEN_REFUSALS:
        return error
    problem, cause = _TOKEN_REFUSALS[error.code]
    server_cause = error.info.cause
    return _error(
        error.code, problem, server_cause if server_cause not in ("", "unknown") else cause,
        _MAKE_ONE,
    )


def hint(status: dict[str, Any]) -> str:
    """The token's hint as Hugging Face tokens look: hf_…abcd."""
    value = str(status.get("token_hint") or "")
    return value if not value or "…" in value or value.startswith("hf_") else f"hf_…{value}"


def _role(status: dict[str, Any]) -> str:
    role = str(status.get("role") or "read")
    return "fine-grained, read-only" if role == "fineGrained" else role


def _ago(value: Any, now: datetime | None = None) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        then = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if then.tzinfo is None:
        then = then.replace(tzinfo=UTC)
    seconds = max(((now or datetime.now(UTC)) - then).total_seconds(), 0)
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{int(seconds // 60)} min ago"
    if seconds < 86400:
        return f"{int(seconds // 3600)} h ago"
    if seconds < 30 * 86400:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    return f"on {then.date().isoformat()}"


def status_lines(status: dict[str, Any], *, now: datetime | None = None) -> list[str]:
    """What `status` prints: the account and token, a refused token's fix, or how to connect."""
    if not status.get("connected"):
        return [
            "Hugging Face isn't connected. Public repos work without it.",
            f"Connect it for your private repos: {SETUP_COMMAND}",
        ]
    user = status.get("username") or "your account"
    oauth = status.get("kind") == "oauth"
    if status.get("failed_at"):
        return errors.ErrorInfo(
            "hf_token_failed",
            f"Hugging Face refused the access connected for {user} (signed in with Hugging "
            "Face)" if oauth else
            f"Hugging Face refused the token connected for {user} ({hint(status)})",
            f"it was revoked or expired {_ago(status['failed_at'], now) or ''}".rstrip(),
            f"rerun `{SETUP_COMMAND}`" if oauth else _MAKE_ONE,
        ).render().splitlines()
    used = _ago(status.get("last_used_at"), now)
    lines = [f"✓ Hugging Face: connected as {user}"]
    if status.get("orgs"):
        lines.append(f"  orgs:  {', '.join(map(str, status['orgs']))}")
    lines.append(
        ("  access: signed in with Hugging Face · read-only · " if oauth else
         f"  token: {hint(status)} · {_role(status)} · ")
        + (f"last used {used}" if used else "not used yet")
    )
    return lines


def _fingerprint(status: dict[str, Any]) -> tuple:
    """What changes when a connection is made or replaced."""
    return tuple(status.get(key) for key in (
        "connected", "kind", "username", "token_hint", "created_at", "failed_at",
    ))


def run_setup(
    *,
    token: str | None = None,
    paste: bool = False,
    client_factory: Callable[..., Any] | None = None,
    print_fn: Callable[[str], None] = print,
    prompt: Callable[[str], str] = getpass.getpass,
    open_browser: Callable[[str], bool] = webbrowser.open,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
    wait_s: float = WAIT_S,
) -> dict[str, Any]:
    """Connect Hugging Face to your Dreamscale account: sign in with Hugging Face in the
    dashboard where that is offered, else (or with --token / --paste) a read token. Returns
    the status."""
    config = load_config()
    if not config.api_key:
        raise errors.catalog("not_configured")
    if token is None and not paste:
        before = _call(client_factory, "hugging_face_status")
        link = dashboard_url(CONNECT_PATH, config.control_plane_url)
        if before.get("oauth") and link:
            return _sign_in(
                before, link, client_factory=client_factory, print_fn=print_fn,
                open_browser=open_browser, sleep=sleep, clock=clock, wait_s=wait_s,
            )
    if token is None:
        print_fn(f"Create a token with the Read role at {NEW_TOKEN_URL}")
        token = prompt("Hugging Face read token: ")
    token = token.strip()
    if not token:
        raise _error(
            "hugging_face_token_missing",
            "no token was given",
            "the prompt was left empty",
            f"rerun `{SETUP_COMMAND}` and paste a read token",
        )
    try:
        status = _call(client_factory, "connect_hugging_face", token)
    except errors.DreamscaleError as error:
        raise _refusal(error) from error
    _forget_local_token()
    print_fn(
        f"✓ Connected Hugging Face as {status.get('username') or 'your account'}. "
        "Deployments and training read your private repos with it."
    )
    return status


def _sign_in(
    before: dict[str, Any],
    link: str,
    *,
    client_factory: Callable[..., Any] | None,
    print_fn: Callable[[str], None],
    open_browser: Callable[[str], bool],
    sleep: Callable[[float], None],
    clock: Callable[[], float],
    wait_s: float,
) -> dict[str, Any]:
    """Open the dashboard's Connect Hugging Face (Hugging Face's consent screen) and wait for
    the connection to appear or change."""
    print_fn("Sign in with Hugging Face to connect it (read-only):")
    print_fn(f"  {link}")
    try:
        opened = open_browser(link)
    except Exception:  # noqa: BLE001 - no browser here (SSH, a container): the link is printed
        opened = False
    if not opened:
        print_fn("Open the link in a browser signed in to Dreamscale.")
    print_fn(f"Waiting for the connection… (Ctrl-C to stop; or `{SETUP_COMMAND} --paste`)")
    seen = _fingerprint(before)
    deadline = clock() + wait_s
    while clock() < deadline:
        sleep(POLL_S)
        status = _call(client_factory, "hugging_face_status")
        if status.get("connected") and not status.get("failed_at") and (
            _fingerprint(status) != seen
        ):
            _forget_local_token()
            print_fn(
                f"✓ Connected Hugging Face as {status.get('username') or 'your account'}. "
                "Deployments and training read your private repos with it."
            )
            return status
    raise _error(
        "hugging_face_not_connected",
        "Hugging Face wasn't connected",
        f"no sign-in finished within {int(wait_s // 60)} minutes",
        f"open {link} and rerun `{SETUP_COMMAND}`, or connect a read token with "
        f"`{SETUP_COMMAND} --paste`",
    )


def run_status(
    *,
    client_factory: Callable[..., Any] | None = None,
    print_fn: Callable[[str], None] = print,
) -> dict[str, Any]:
    status = _call(client_factory, "hugging_face_status")
    for line in status_lines(status):
        print_fn(line)
    return status


def _ask(prompt: str) -> bool:
    import click

    try:
        return click.confirm(prompt, default=False, err=True)
    except click.Abort:
        return False


def run_remove(
    *,
    yes: bool = False,
    client_factory: Callable[..., Any] | None = None,
    print_fn: Callable[[str], None] = print,
    confirm_fn: Callable[[str], bool] = _ask,
    interactive: bool | None = None,
) -> dict[str, Any]:
    """Disconnect Hugging Face: Dreamscale deletes the token."""
    status = _call(client_factory, "hugging_face_status")
    if not status.get("connected"):
        _forget_local_token()
        print_fn("Hugging Face isn't connected; nothing to remove.")
        return status
    user = status.get("username") or "your account"
    if not yes:
        if not (sys.stdin.isatty() if interactive is None else interactive):
            raise _error(
                "confirm_required",
                "removing the Hugging Face connection needs a yes, and there is no terminal "
                "to ask in",
                "stdin isn't a terminal (a script, a pipe or an agent)",
                "rerun `dreamscale integrations hugging-face remove --yes`",
            )
        print_fn("Deployments and training will stop reading your private repos.")
        if not confirm_fn(f"Disconnect Hugging Face ({user})?"):
            print_fn("Still connected.")
            return status
    status = _call(client_factory, "disconnect_hugging_face")
    _forget_local_token()
    print_fn(f"✓ Disconnected Hugging Face ({user}). Dreamscale deleted the token.")
    return status
