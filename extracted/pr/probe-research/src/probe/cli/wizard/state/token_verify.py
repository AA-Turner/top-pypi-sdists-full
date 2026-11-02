"""verify a pasted or held token with the API and fingerprint it (probe mcp token set/status and the daemon-key check)."""

from __future__ import annotations
import hashlib

import typer

from .... import __version__, errors
from ....foundation.request_identity.request_identity import client_version_headers
from ....sdk.settings.settings import resolve
from ....foundation.request_identity.surface import Surface


def _normalize_token(raw: str) -> str:
    """Undo how tokens actually arrive: pasted with `Bearer `, quotes, or a newline."""
    token = raw.strip()
    for _ in range(2):  # e.g. "Bearer probe_pat_x" needs both peels
        if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
            token = token[1:-1].strip()
        if token.lower().startswith("bearer "):
            token = token[7:].strip()
    return token


def _checked_token(raw: str) -> str:
    token = _normalize_token(raw)
    if not token:
        # These used to raise the standalone click's BadParameter to dodge the bug
        # main() now fixes at the root (see the ClickException note above): typer's own
        # BadParameter is caught correctly, so the workaround is gone.
        raise typer.BadParameter("token is empty")
    # No prefix check: the server takes both `ros_pat_` and `probe_pat_`, and the
    # prefix is only a discriminator — real auth is a sha256 lookup.
    if any(c.isspace() or ord(c) < 32 for c in token):
        raise typer.BadParameter("token contains whitespace or control characters")
    return token


def _fingerprint(token: str) -> str:
    """Enough to compare two tokens without printing either."""
    return f"…{token[-4:]} (sha256:{hashlib.sha256(token.encode()).hexdigest()[:8]})"


def _verify(token: str, base_url: str) -> tuple[str, dict | None]:
    """Ask the API who this token is. Returns (state, identity).

    state: ``ok`` | ``rejected`` (definitive 401/403) | ``unreachable`` (blip).
    """
    try:
        with _new_client(base_url=base_url, token=token, fail_open=False) as client:
            return "ok", client.me()
    except (errors.AuthError, errors.ScopeError):  # 401, 403 — both definitive
        return "rejected", None
    except (errors.TransportError, errors.ServerError):
        return "unreachable", None


def _verify_read(token: str, base_url: str) -> tuple[str, dict | None]:
    """`_verify` through the SDK's transport alone, with the same answers: a
    `Client` imports every wire model (~0.5 s), and the wizard asks this under
    its first spinner (`capabilities.ask_mcp_token_verdict`)."""
    from ....sdk.delivery.transport.transport import Transport

    settings = resolve(base_url=base_url, token=token)
    try:
        with Transport(
            settings,
            surface=Surface.CLI.value,
            client_headers=client_version_headers("cli", __version__),
        ) as transport:
            return "ok", transport.get("/v1/me")
    except (errors.AuthError, errors.ScopeError):  # 401, 403 — both definitive
        return "rejected", None
    except (errors.TransportError, errors.ServerError):
        return "unreachable", None
from probe.cli.connection import _new_client  # noqa: E402 -- pieces need each other; the front door loads this one first
