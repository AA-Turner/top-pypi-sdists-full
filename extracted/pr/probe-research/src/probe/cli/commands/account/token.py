"""probe token list/create/revoke: API tokens minted through the device flow."""

from __future__ import annotations
import sys

import typer
# The option enums only, from `_generated.enums` rather than `probe.models`: that
# seam builds every wire model, ~0.5 s that every command paid at startup -- the
# wizard, the hooks and the status line included -- whether or not it sent one.
# `tests/test_cli_startup_imports.py` holds the CLI to this.
from ....generated.enums import Scope
from ....sdk.settings.device import DeviceLoginError


# -- tokens -----------------------------------------------------------------
token_app = typer.Typer(no_args_is_help=True, help="API tokens (probe_pat_...)")


@token_app.command("list")
def token_list() -> None:
    """List my live tokens. Secrets are never shown — match on `token_prefix`."""
    with _client() as c:
        _print_json(c.list_tokens())


@token_app.command("create")
def token_create(
    name: str = typer.Option(..., "--name", help="what this token is for, e.g. 'ci-bot'"),
    scope: list[Scope] = typer.Option(
        None,
        "--scope",
        help="repeatable; omit to request read+write+delete (never admin). A token can "
        "never exceed the scopes your role confers.",
    ),
    no_browser: bool = typer.Option(
        False, "--no-browser", help="print the URL instead of opening it"
    ),
) -> None:
    """Mint a token via the browser device flow — approve in the dashboard.

    Minting deliberately requires a human in a browser (a leaked token must not be
    able to mint more tokens), so this prints a URL + code and waits for approval.
    The secret is printed ONCE and never stored; copy it now.
    """
    from probe.cli.wizard.account.device_prompt import _show_device_prompt
    # PRB-002: the device flow no longer grants admin (the server refuses it), so
    # fail fast with a clear message instead of a round-trip to a 400. Admin
    # tokens must be minted from a signed-in session.
    if scope and Scope.admin in scope:
        print(
            "admin tokens can't be minted from the CLI; mint one from a signed-in session.",
            file=sys.stderr,
        )
        raise typer.Exit(2)
    with _client() as c:
        print(f"opening {c.settings.base_url} for browser approval…")
        try:
            created = c.create_token(
                name,
                scopes=[s.value for s in scope] if scope else None,
                open_browser=not no_browser,
                on_prompt=_show_device_prompt,
            )
        except DeviceLoginError as exc:
            print(f"token creation failed: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc

    # The token is already minted server-side; its plaintext exists exactly once. Read
    # the secret FIRST so a missing name/id (response drift) can't KeyError before it is
    # shown and orphan an unrecoverable token. name/id are decorative — fall back.
    secret = created["token"]
    label = created.get("name", name)
    token_id = created.get("id", "unknown")
    # Shown once, and only here: not via _print_json (which invites piping it to a
    # file) and never written to config.
    print(f"\ntoken {label!r} created (id: {token_id})")
    print(f"\n  {secret}\n")
    print("^ copy it now — this is the only time it is shown.", file=sys.stderr)


@token_app.command("revoke")
def token_revoke(
    token_id: str = typer.Argument(..., help="token id (from `probe token list`)"),
) -> None:
    """Revoke one of my tokens. Revoking a teammate's needs the dashboard."""
    with _client() as c:
        c.revoke_token(token_id)
    print(f"revoked {token_id}")
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
