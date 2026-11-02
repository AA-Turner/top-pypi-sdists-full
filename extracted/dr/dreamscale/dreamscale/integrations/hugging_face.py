"""Hugging Face: one read token per user, kept by Dreamscale, for private repos.

`dreamscale integrations hugging-face setup` asks for a read token (or takes --token) and
sends it to the control plane, which checks it with Hugging Face, refuses one that can write
and keeps it (encrypted) for your account: the dashboard's Integrations page shows and
changes the same connection. Deployments (inspect, create) and training then read your
private repos with it. `status` shows the connection; `remove` deletes the token.

A request's own token wins: --hf-token, then HF_TOKEN. Without either the SDK sends none and
the control plane uses the connected one.
"""

from __future__ import annotations

import asyncio
import getpass
import os
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from dreamscale import errors
from dreamscale.config import load_config, save_config
from dreamscale.control import ControlPlaneClient

NAME = "hugging-face"
NEW_TOKEN_URL = "https://huggingface.co/settings/tokens/new?tokenType=read"
SETUP_COMMAND = "dreamscale integrations hugging-face setup"
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
    if status.get("failed_at"):
        return errors.ErrorInfo(
            "hf_token_failed",
            f"Hugging Face refused the token connected for {user} ({hint(status)})",
            f"it was revoked or expired {_ago(status['failed_at'], now) or ''}".rstrip(),
            _MAKE_ONE,
        ).render().splitlines()
    used = _ago(status.get("last_used_at"), now)
    lines = [f"✓ Hugging Face: connected as {user}"]
    if status.get("orgs"):
        lines.append(f"  orgs:  {', '.join(map(str, status['orgs']))}")
    lines.append(
        f"  token: {hint(status)} · {_role(status)} · "
        + (f"last used {used}" if used else "not used yet")
    )
    return lines


def run_setup(
    *,
    token: str | None = None,
    client_factory: Callable[..., Any] | None = None,
    print_fn: Callable[[str], None] = print,
    prompt: Callable[[str], str] = getpass.getpass,
) -> dict[str, Any]:
    """Ask for a read token and connect it to your Dreamscale account. Returns the status."""
    if not load_config().api_key:
        raise errors.catalog("not_configured")
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
