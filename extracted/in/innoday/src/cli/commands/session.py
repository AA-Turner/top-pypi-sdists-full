"""
InnoDay CLI session-authentication commands: `login`, `logout`, `whoami`.

These implement the OAuth 2.0 device-authorization flow against the InnoDay
API so a developer can authenticate the CLI the same way `gh auth login` or
`railway login` work — no manually-pasted headers. The resulting typed token
(`ido_...` for device login, `idt_...` for a PAT; see `src/domain/cli_token.py`)
is stored in the OS keyring (see `CLIConfig.store_cli_token`) and sent as
`Authorization: Bearer <token>` on every subsequent request (see
`src/cli/client.py`).

The `/device/*` endpoints are unauthenticated, so they're called with a plain
httpx client rather than `InnoDayAPIClient` (which injects identity headers).
Authenticated calls (`/auth/me`, token revocation) go through httpx directly
too, with an explicit bearer header, to keep this module self-contained.
"""

import argparse
import asyncio
import sys
import time
import webbrowser
from typing import Any, Dict, Optional, Tuple

import httpx
from rich.console import Console
from rich.panel import Panel

from src.cli.config import CLIConfig
from src.cli.utils.formatters import format_error, format_success, format_warning

console = Console()

# OAuth device-flow grant type per RFC 8628.
DEVICE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"
# Public client identifier for the CLI (the device flow has no client secret).
CLI_CLIENT_ID = "innoday-cli"
DEFAULT_SCOPE = "cli"
DEFAULT_POLL_TIMEOUT = 300.0


def _base_url(config: CLIConfig, override: Optional[str] = None) -> str:
    return (override or config.get_api_url()).rstrip("/")


async def _health_ok(base_url: str) -> bool:
    """Best-effort liveness check against the unauthenticated /health route."""
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
            response = await client.get(f"{base_url}/health")
            return response.status_code == 200
    except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError):
        return False


async def _fetch_me(
    base_url: str, token: str, team_secret: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Return the /auth/me payload for a token, or None if it isn't valid.

    On a team-secret-gated deployment (dev/prod with ``TEAM_ACCESS_SECRET``
    set) every non-exempt route — including ``/api/v1/auth/me`` — is behind
    ``TeamSecretMiddleware``, which rejects the request *before* auth runs when
    the ``X-Team-Secret`` header is absent. So we attach it (same convention as
    ``InnoDayAPIClient``) whenever the CLI has one configured; otherwise the
    server would 401 a perfectly valid token and login would look "rejected".
    """
    headers = {"Authorization": f"Bearer {token}"}
    if team_secret:
        headers["X-Team-Secret"] = team_secret
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
            response = await client.get(
                f"{base_url}/api/v1/auth/me",
                headers=headers,
            )
        if response.status_code == 200:
            return response.json()
        return None
    except httpx.HTTPError:
        return None


def _identity_line(me: Dict[str, Any]) -> str:
    name = me.get("full_name") or me.get("name") or "unknown"
    email = me.get("email") or ""
    return f"{name} ({email})" if email else name


def _persist_user(config: CLIConfig, user: Dict[str, Any]) -> bool:
    """Mirror the identity into config.json so status/whoami work offline too.

    Uses the same setter `init` relies on; tolerant of partial payloads
    (the /device/token user block and /auth/me differ slightly in shape).

    Returns True when it wrote. A no-op when the stored identity already
    matches, because `whoami` calls this on every run (#619) and an
    unconditional `save()` would print "Configuration saved to ..." each time
    and rewrite the shared config file for nothing.
    """
    user_id = user.get("id")
    email = user.get("email")
    name = user.get("full_name") or user.get("name")
    if not user_id:
        return False
    stored = config.get_user_info()
    if (stored.get("id"), stored.get("email"), stored.get("name")) == (
        user_id,
        email,
        name,
    ):
        return False
    config.set_user_info(user_id, email, name)
    config.save()
    return True


class SessionCommands:
    """`login` / `logout` / `whoami` handlers."""

    # ------------------------------------------------------------------
    # login
    # ------------------------------------------------------------------

    @staticmethod
    def setup_login_parser(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--with-token",
            action="store_true",
            help="Read an existing token from stdin instead of running the "
            "browser device flow (useful for CI).",
        )
        parser.add_argument("--api-url", metavar="URL", help="Override API URL")
        mode = parser.add_mutually_exclusive_group()
        mode.add_argument(
            "--web",
            dest="web",
            action="store_true",
            default=True,
            help="Open a browser to complete login (default).",
        )
        mode.add_argument(
            "--device",
            dest="web",
            action="store_false",
            help="Code-only flow; do not attempt to open a browser.",
        )
        parser.add_argument(
            "--timeout",
            type=float,
            default=DEFAULT_POLL_TIMEOUT,
            help=f"Overall polling timeout in seconds (default: {int(DEFAULT_POLL_TIMEOUT)}).",
        )

    @staticmethod
    async def login(args: argparse.Namespace, config: CLIConfig) -> int:
        base_url = _base_url(config, getattr(args, "api_url", None))

        if not await _health_ok(base_url):
            console.print(
                format_error(
                    f"Cannot reach InnoDay at {base_url}. Is the server running? "
                    "Try 'innoday platform start' or check --api-url."
                )
            )
            return 1

        # --with-token: validate a pasted/piped token and store it.
        if getattr(args, "with_token", False):
            return await SessionCommands._login_with_token(base_url, config)

        # Already authenticated? Skip the flow.
        existing = config.get_cli_token()
        if existing:
            me = await _fetch_me(base_url, existing, config.get_team_secret())
            if me:
                console.print(
                    format_success(f"Already logged in as {_identity_line(me)}")
                )
                return 0

        return await SessionCommands._login_device_flow(args, base_url, config)

    @staticmethod
    async def _login_with_token(base_url: str, config: CLIConfig) -> int:
        console.print(
            "[dim]Paste your InnoDay token, then Enter (or pipe via stdin):[/dim]"
        )
        token = sys.stdin.readline().strip()
        if not token:
            console.print(format_error("No token provided on stdin."))
            return 1

        me = await _fetch_me(base_url, token, config.get_team_secret())
        if not me:
            console.print(
                format_error(
                    "Token rejected by the server (/auth/me returned no user).\n"
                    "If this API is team-secret gated, set the team secret first:\n"
                    "  innoday config set team-secret <value>"
                )
            )
            return 1

        config.store_cli_token(token)
        _persist_user(config, me)
        console.print(format_success(f"Logged in as {_identity_line(me)}"))
        return 0

    @staticmethod
    async def _request_device_code(
        base_url: str,
    ) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
                response = await client.post(
                    f"{base_url}/api/v1/device/code",
                    json={"client_id": CLI_CLIENT_ID, "scope": DEFAULT_SCOPE},
                )
            if response.status_code != 200:
                console.print(
                    format_error(
                        f"Device code request failed (HTTP {response.status_code}): "
                        f"{response.text[:200]}"
                    )
                )
                return None
            return response.json()
        except httpx.HTTPError as exc:
            console.print(format_error(f"Device code request failed: {exc}"))
            return None

    @staticmethod
    def _show_device_prompt(device: Dict[str, Any], open_browser: bool) -> None:
        user_code = device.get("user_code", "?")
        verification_uri = device.get("verification_uri", "")
        verification_uri_complete = device.get("verification_uri_complete")

        console.print(
            Panel(
                f"[bold]Your one-time code:[/bold]  [bold cyan]{user_code}[/bold cyan]\n\n"
                f"Visit [link]{verification_uri}[/link] and enter the code above.",
                title="🔐 InnoDay Login",
                border_style="cyan",
            )
        )

        if open_browser and verification_uri_complete:
            try:
                opened = webbrowser.open(verification_uri_complete)
            except Exception:
                opened = False
            if opened:
                console.print("[dim]Opening your browser to complete login…[/dim]")
            else:
                console.print(
                    "[dim]Couldn't open a browser — visit the URL above manually.[/dim]"
                )

    @staticmethod
    async def _poll_for_token(
        base_url: str,
        device_code: str,
        interval: float,
        deadline: float,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Poll /device/token until approval, denial, or timeout.

        Returns (token_payload, error_string). Exactly one is non-None.
        """
        current_interval = max(interval, 1.0)
        async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
            while time.monotonic() < deadline:
                await asyncio.sleep(current_interval)
                try:
                    response = await client.post(
                        f"{base_url}/api/v1/device/token",
                        json={
                            "grant_type": DEVICE_GRANT_TYPE,
                            "device_code": device_code,
                        },
                    )
                except httpx.HTTPError as exc:
                    # Transient network hiccup — keep polling until deadline.
                    console.print(f"[dim]Polling error ({exc}); retrying…[/dim]")
                    continue

                if response.status_code == 200:
                    return response.json(), None

                error = SessionCommands._extract_oauth_error(response)
                if error == "authorization_pending":
                    continue
                if error == "slow_down":
                    current_interval += 5
                    continue
                if error in ("access_denied", "expired_token", "invalid_grant"):
                    return None, error
                # Unknown error shape — surface it and stop.
                return None, error or f"HTTP {response.status_code}"

        return None, "timeout"

    @staticmethod
    def _extract_oauth_error(response: httpx.Response) -> Optional[str]:
        """Pull the OAuth error slug out of a 400 body: {"detail": {"error": ...}}."""
        try:
            body = response.json()
        except ValueError:
            return None
        detail = body.get("detail", body)
        if isinstance(detail, dict):
            return detail.get("error")
        if isinstance(detail, str):
            return detail
        return None

    @staticmethod
    async def _login_device_flow(
        args: argparse.Namespace, base_url: str, config: CLIConfig
    ) -> int:
        device = await SessionCommands._request_device_code(base_url)
        if device is None:
            return 1

        SessionCommands._show_device_prompt(device, bool(getattr(args, "web", True)))

        interval = float(device.get("interval", 5) or 5)
        timeout = float(getattr(args, "timeout", DEFAULT_POLL_TIMEOUT))
        deadline = time.monotonic() + timeout

        console.print("[dim]Waiting for authorization…[/dim]")
        token_payload, error = await SessionCommands._poll_for_token(
            base_url, device["device_code"], interval, deadline
        )

        if error:
            messages = {
                "access_denied": "Login was denied.",
                "expired_token": "The code expired before you approved it. Run 'innoday login' again.",
                "invalid_grant": "The device code is no longer valid. Run 'innoday login' again.",
                "timeout": "Timed out waiting for authorization. Run 'innoday login' again.",
            }
            console.print(format_error(messages.get(error, f"Login failed: {error}")))
            return 1

        token = token_payload.get("access_token")
        if not token:
            console.print(format_error("Server did not return an access token."))
            return 1

        config.store_cli_token(token)
        user = token_payload.get("user") or {}
        _persist_user(config, user)

        name_line = _identity_line(user) if user else "you"
        console.print(format_success(f"Logged in as {name_line}"))
        return 0

    # ------------------------------------------------------------------
    # logout
    # ------------------------------------------------------------------

    @staticmethod
    def setup_logout_parser(parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--api-url", metavar="URL", help="Override API URL")

    @staticmethod
    async def logout(args: argparse.Namespace, config: CLIConfig) -> int:
        base_url = _base_url(config, getattr(args, "api_url", None))
        token = config.get_cli_token()

        # Best-effort server-side revocation. The CLI holds only the raw token,
        # not its id, so we revoke all of the caller's tokens via the
        # revoke-all endpoint. Never fail logout if this call can't complete.
        if token:
            try:
                async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                    await client.delete(
                        f"{base_url}/api/v1/auth/tokens",
                        headers={"Authorization": f"Bearer {token}"},
                    )
            except httpx.HTTPError:
                pass

        config.delete_cli_token()
        console.print(format_success("Logged out."))
        return 0

    # ------------------------------------------------------------------
    # whoami
    # ------------------------------------------------------------------

    @staticmethod
    def setup_whoami_parser(parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--api-url", metavar="URL", help="Override API URL")

    @staticmethod
    async def whoami(args: argparse.Namespace, config: CLIConfig) -> int:
        base_url = _base_url(config, getattr(args, "api_url", None))
        token = config.get_cli_token()

        if not token:
            console.print(format_warning("Not logged in — run `innoday login`."))
            return 1

        me = await _fetch_me(base_url, token, config.get_team_secret())
        if not me:
            console.print(
                format_warning(
                    "Your session is no longer valid — run `innoday login` again."
                )
            )
            return 1

        console.print(f"[bold]{_identity_line(me)}[/bold]")

        # Persist what we just fetched. `whoami` resolved the full identity and
        # then threw all of it away, so a machine holding a valid token but no
        # `user.id` -- the state a non-interactive `config init` used to leave
        # behind -- stayed broken no matter how many times you asked the CLI who
        # you were. Everything reading `get_user_id()` (`board register`,
        # `license`, organizations.py, client.py) now self-heals on the first
        # `whoami` (#619).
        _persist_user(config, me)

        # A legacy/out-of-date .innoday/project.yml doesn't stop whoami: the
        # entrypoint marks whoami legacy-tolerant (allow_legacy_context), so the
        # error is recorded rather than raised. Show whatever org context still
        # resolves, then warn (in red) to run `innoday refresh`.
        current_org = config.get_current_organization()
        if current_org:
            console.print(f"[dim]Current org (from cwd):[/dim] {current_org}")

        orgs = me.get("organizations") or []
        if orgs:
            names = ", ".join(o.get("alias") or o.get("name", "?") for o in orgs)
            console.print(f"[dim]Member of:[/dim] {names}")

        if me.get("is_platform_member"):
            console.print("[dim]Platform member:[/dim] yes")

        SessionCommands._print_identities(me.get("identities") or [])

        if config.legacy_context_error:
            console.print(
                format_error(
                    "Your project config is out of date — run `innoday refresh` "
                    "to update this workspace."
                )
            )

        return 0

    @staticmethod
    def _print_identities(identities: list) -> None:
        """Which board handles InnoDay believes are you (PF-398). Read-only.

        Printed here because `whoami` is where someone already goes to ask "who
        does this thing think I am?", and the board handle is the half of that
        answer which decides whether `innoday summary` can find their work at
        all. Having none is the interesting case, so it gets the loud line and
        the fix rather than being rendered as an empty list.
        """
        from rich.markup import escape

        if not identities:
            console.print(
                "[yellow]Board identities:[/yellow] none — "
                "your board work can't be attributed to you until one is mapped "
                "(map it on your profile page)"
            )
            return

        console.print("[dim]Board identities:[/dim]")
        for identity in identities:
            handle = escape(str(identity.get("handle") or "?"))
            platform = escape(str(identity.get("platform") or "?"))
            # "global" is a real answer, not a blank -- it is the handle
            # auto-matching draws from everywhere, so name it as such.
            scope = identity.get("project") or identity.get("scope") or "global"
            console.print(f"  {platform}: @{handle} [dim]({escape(str(scope))})[/dim]")
