"""probe mcp ...: the read-only MCP token (set/unset/status), its header and env forms, and the inline tools/call bridge."""

from __future__ import annotations
import json
import os
import shlex
import sys
from pathlib import Path
from typing import Optional

import typer

from .... import errors
from ....sdk.settings.settings import (
    config_path,
    load_context,
    resolve,
    save_context)
from ....sdk import session_marker
from ....sdk.settings.device import (
    DeviceLoginError,
    credentials_by_grant,
    device_authorize,
    hostname)


# -- mcp read credential ----------------------------------------------------
class _McpGroup(typer.core.TyperGroup):
    """`probe mcp`, whose typo suggestions name only its listed commands.

    Typer answers `probe mcp tool` with "Did you mean 'tools'?" from EVERY
    subcommand, hidden ones included, so a typo outside `/probe inline` would
    advertise the inline-only `tools`/`call` that `--help` hides. Suggest from
    the visible commands instead (older Typer, which suggests nothing, gains the
    same visible-only suggestion)."""

    def resolve_command(self, ctx, args):  # type: ignore[override]
        import difflib

        self.suggest_commands = False  # Typer's own suggestion lists hidden commands too
        try:
            return super().resolve_command(ctx, args)
        except UsageError as exc:  # Typer's own click's (module top), never `import click`
            visible = [name for name, command in self.commands.items() if not command.hidden]
            matches = difflib.get_close_matches(args[0], visible) if args else []
            if matches:
                suggestions = ", ".join(repr(match) for match in matches)
                exc.message = f"{exc.message.rstrip('.')}. Did you mean {suggestions}?"
            raise


mcp_app = typer.Typer(
    cls=_McpGroup, no_args_is_help=True, help="the read-only credential the MCP surface uses"
)

mcp_token_app = typer.Typer(no_args_is_help=True, help="manage the read-only MCP token")
mcp_app.add_typer(mcp_token_app, name="token")

_READ_ONLY_SCOPES = {"read"}


@mcp_token_app.command("set")
def mcp_token_set(
    token: str = typer.Option(None, "--token", help="paste a read-only token (air-gap path)"),
    allow_write: bool = typer.Option(False, "--allow-write", help="persist even if it can write"),
    verify: bool = typer.Option(
        True, "--verify/--no-verify", help="check the token against /v1/me"
    ),
) -> None:
    """Store the read-only token the MCP uses. Re-run to rotate — it replaces, never appends.

    Bare `probe mcp token set` mints a read-only token in the browser, so nothing is
    pasted and no secret lands in your shell history or `ps` output.
    """
    from probe.cli.wizard.account.device_prompt import _show_device_prompt
    from probe.cli.wizard.state.token_verify import _checked_token, _fingerprint, _verify
    base = resolve(base_url=_conn.base_url).base_url
    if token is not None:
        # `--token ""` is a mistake to report, not a cue to open a browser.
        secret = _checked_token(token)
    else:
        print(f"opening {base} to mint a read-only token…")
        try:
            # Ask for the `mcp` capability by name. Omitting `grants` takes the
            # server default of `["api"]`, which minted this read-only credential
            # tagged as an API credential under an installation of its own -- so
            # one laptop showed up as two machines, and `installation_role` said
            # nothing true about what the credential could do.
            #
            # `token_name` is the ORDINARY CLI shape on purpose: the server
            # appends " (MCP)" to the credential and names the installation after
            # the bare value, so this yields the same canonical device name every
            # other pairing produces instead of a third spelling of one machine.
            minted = device_authorize(
                base,
                scopes=["read"],
                grants=["mcp"],
                token_name=f"Probe Research CLI · {hostname()}",
                on_prompt=_show_device_prompt,
            )
        except DeviceLoginError as exc:
            print(f"device login failed: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc
        # Not device_login(): that returns the response's top-level `token`,
        # which only exists when an `api` grant was requested. With `mcp` alone
        # the credential rides in `grants`.
        credential = credentials_by_grant(minted).get("mcp") or {}
        secret = credential.get("token")
        if not secret:
            print(
                "error: the server did not return an MCP credential. It may predate "
                "the `mcp` grant; upgrade the backend or pass --token.",
                file=sys.stderr,
            )
            raise typer.Exit(1)

    state, identity = _verify(secret, base) if verify else ("skipped", None)
    if state == "rejected":
        # Persisting a token the API already refuses just moves the failure somewhere
        # quieter — the MCP would load its tools and fail every call.
        print("error: the API rejected this token; nothing was saved", file=sys.stderr)
        raise typer.Exit(1)

    scopes = set((identity or {}).get("scopes") or [])
    if scopes and not scopes <= _READ_ONLY_SCOPES and not allow_write:
        print(
            f"error: this token carries {sorted(scopes)}; the MCP credential should be read-only.\n"
            "       Mint a read-only one with `probe mcp token set` (no --token), "
            "or pass --allow-write to override.",
            file=sys.stderr,
        )
        raise typer.Exit(1)

    updates = {"mcp_token": secret}
    if not load_context().get("base_url"):
        updates["base_url"] = base
    path = save_context(updates)

    # Codex holds its own copy of this token in ~/.codex/config.toml. Leaving
    # the old one there is a silent 401 on every Codex call, with a health check
    # that still says authenticated.
    from probe.cli import wizard as _wizard

    for line in _wizard.sync_mcp_token():
        print(line)

    who = (identity or {}).get("email") or "unverified"
    # Never report success without saying whether it was actually checked — an
    # unverified write that reads like a verified one is how this broke before.
    note = {
        "ok": f"verified: yes ({who}, scopes={sorted(scopes) or 'unknown'})",
        "unreachable": "verified: no (API unreachable — run `probe mcp status` to recheck)",
        "skipped": "verified: no (--no-verify)",
    }[state]
    print(f"saved mcp_token {_fingerprint(secret)} to {path}\n{note}")
    if scopes and not scopes <= _READ_ONLY_SCOPES:
        print("warning: this token can write; the MCP surface is read-only by design")
    elif state != "ok":
        # The read-only guard runs on the verified path only. Say so, rather than let
        # an unchecked token look like a checked one that passed.
        print("warning: scopes unchecked — this token may be able to write")
    print("Restart any MCP client that is already running, or reconnect it, to pick this up.")


@mcp_token_app.command("unset")
def mcp_token_unset() -> None:
    """Remove the stored read-only MCP token."""
    if not load_context().get("mcp_token"):
        print("no mcp_token stored")
        return
    print(f"removed mcp_token from {save_context({'mcp_token': None})}")


@mcp_app.command("headers")
def mcp_headers() -> None:
    """Emit the MCP Authorization header as JSON (for a client's headers helper)."""
    settings = resolve(base_url=_conn.base_url)
    if not settings.mcp_token:
        print(
            f"no MCP token: set PROBE_MCP_TOKEN, or the wizard's Install mints one ({session_marker.WIZARD_HINT})",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    from ....sdk.settings import workspace_limit as wl

    headers = {"Authorization": f"Bearer {settings.mcp_token}"}
    try:
        headers.update(wl.headers_for(settings, bearer=settings.mcp_token))
    except errors.RosError as exc:
        # Never dropped (that would widen it): a limit this cannot name goes as
        # found, and the API refuses it with a message naming the fix.
        print(f"warning: {exc}", file=sys.stderr)
        headers.update(wl.fail_closed_headers(settings.workspace_limit))
    print(json.dumps(headers))


@mcp_app.command("env")
def mcp_env() -> None:
    """Print the export line, for MCP clients that only read the environment.

    Prints a secret to stdout. Nothing is written to a shell profile: a tool that
    edits rc files it did not author breaks `export X=$(op read …)` and compound
    statements. Add the line yourself, or use a client that supports a headers helper.
    """
    settings = resolve(base_url=_conn.base_url)
    if not settings.mcp_token:
        print(f"no MCP token: the wizard's Install mints one ({session_marker.WIZARD_HINT})", file=sys.stderr)
        raise typer.Exit(1)
    print(f"export PROBE_MCP_TOKEN={shlex.quote(settings.mcp_token)}")


def _stale_literal_copies(token: str | None) -> list[str]:
    """Places that pin a *different* literal token and would outlive a rotation."""
    path = Path.home() / ".claude.json"
    try:
        servers = json.loads(path.read_text()).get("mcpServers") or {}
    except (OSError, json.JSONDecodeError, AttributeError):
        return []
    stale = []
    for name, config in servers.items():
        if not isinstance(config, dict):
            continue
        pinned = [
            (config.get("env") or {}).get("PROBE_MCP_TOKEN"),
            (config.get("headers") or {}).get("Authorization"),
        ]
        for value in pinned:
            if isinstance(value, str) and "pat_" in value and (not token or token not in value):
                stale.append(f"~/.claude.json -> mcpServers.{name}")
                break
    return stale


@mcp_app.command("status")
def mcp_status() -> None:
    """Diagnose the MCP credential: where it comes from, whether it still works."""
    from probe.cli.wizard.state.token_verify import _fingerprint, _verify
    settings = resolve(base_url=_conn.base_url)
    file_token = load_context().get("mcp_token")
    env_token = os.environ.get("PROBE_MCP_TOKEN")
    token = settings.mcp_token

    print(f"config:   {config_path()}")
    print(f"endpoint: {settings.base_url}")
    if not token:
        print(f"token:    none — the wizard's Install mints one ({session_marker.WIZARD_HINT})")
        raise typer.Exit(1)

    source = "environment (PROBE_MCP_TOKEN)" if env_token else "config file"
    print(f"token:    {_fingerprint(token)} from {source}")
    if env_token and file_token and env_token != file_token:
        # The env wins, so a freshly-rotated config token is not what the MCP sends.
        print("          ! the environment and config hold DIFFERENT tokens; the environment wins")
        print(
            f"          config holds {_fingerprint(file_token)} — open a new shell, or unset PROBE_MCP_TOKEN"
        )

    state, identity = _verify(token, settings.base_url)
    if state == "ok":
        scopes = sorted((identity or {}).get("scopes") or [])
        print(f"verify:   ok — {identity.get('email')} scopes={scopes}")
        if set(scopes) - _READ_ONLY_SCOPES:
            print("          ! this token can write; the MCP surface is read-only by design")
    elif state == "rejected":
        print("verify:   REJECTED — the API refuses this token. `probe wizard --action login` "
              "signs in again and replaces it")
    else:
        print("verify:   unknown — the API was unreachable")

    for place in _stale_literal_copies(token):
        print(f"stale:    ! {place} pins a different token and takes precedence over this one")

    if state == "rejected":
        raise typer.Exit(1)


# The hosted Probe MCP from the shell, for `/probe inline` only (`cli/mcp_bridge.py`):
# hidden, and refused in every other session, so nothing outside inline offers them.
MCP_TOOLS_MATCHED = "probe mcp tools"
MCP_CALL_MATCHED = "probe mcp call"


def _mcp_bridge(matched: str):
    """The bridge's target, once this session is inline; else the refusal (exit 2)."""
    from ....shared.reads import mcp_bridge

    refused = mcp_bridge.refusal(matched)
    if refused:
        print(refused, file=sys.stderr)
        raise typer.Exit(mcp_bridge.EXIT_NOT_INLINE)
    try:
        return mcp_bridge, mcp_bridge.target(base_url=_conn.base_url)
    except mcp_bridge.BridgeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise typer.Exit(1) from exc


@mcp_app.command("tools", hidden=True)
def mcp_tools(
    names: Optional[list[str]] = typer.Argument(
        None, help="tools to show in full, with their input schema", show_default=False
    ),
) -> None:
    """The Probe MCP's read guide and tools, as it serves them (`/probe inline` only)."""
    bridge, where = _mcp_bridge(MCP_TOOLS_MATCHED)
    try:
        instructions, tools = bridge.list_tools(where)
    except bridge.BridgeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise typer.Exit(1) from exc
    try:
        listing = bridge.render_tools(instructions, tools, names or ())
    except KeyError as exc:
        served = ", ".join(tool.name for tool in tools)
        print(f"error: the Probe MCP serves no tool {exc.args[0]} (it serves: {served})", file=sys.stderr)
        raise typer.Exit(1) from exc
    print(listing)


@mcp_app.command("call", hidden=True)
def mcp_call(
    tool: str = typer.Argument(..., help="the tool's name (`probe mcp tools` lists them)"),
    arguments: Optional[str] = typer.Argument(
        None, help="its arguments, as one JSON object (default {})", show_default=False
    ),
    args_file: Optional[str] = typer.Option(
        None, "--args-file", help="read the JSON arguments from this file, or - for stdin"
    ),
) -> None:
    """Call one Probe MCP tool and print what it returns (`/probe inline` only)."""
    bridge, where = _mcp_bridge(MCP_CALL_MATCHED)
    if arguments is not None and args_file is not None:
        raise typer.BadParameter("give the arguments OR --args-file, not both")
    raw = arguments
    if args_file is not None:
        try:
            raw = sys.stdin.read() if args_file == "-" else Path(args_file).read_text(encoding="utf-8")
        except OSError as exc:
            raise typer.BadParameter(f"cannot read {args_file}: {exc}") from exc
    try:
        payload = bridge.parse_arguments(raw)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    try:
        result = bridge.call_tool(where, tool, payload)
    except bridge.BridgeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise typer.Exit(1) from exc
    text = bridge.result_text(result)
    if result.isError:
        print(text or f"error: {tool} failed", file=sys.stderr)
        raise typer.Exit(1)
    print(text)
from probe.cli.commands.commands import UsageError  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
