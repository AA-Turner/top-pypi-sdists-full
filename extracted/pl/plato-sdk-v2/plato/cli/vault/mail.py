"""`plato vault mail`: the recovery inboxes (the ``mail-<account>`` items in the ``login`` vault).

The write goes through the login console (``POST /api/logins/mailboxes``). The console holds the
1Password token, so this machine needs no new credential. Chronos serves no ``mail-*`` item
(``plato.chronos.login_vault._1PASSWORD_PREFIXES``), so there is no ``--via chronos``.

The app password is read from stdin or a hidden prompt, never from an argument (argv is visible in
``ps`` and in the shell history). It is never printed, also not in an error text.
"""

from __future__ import annotations

import imaplib
import os
import ssl
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Annotated, Any, NoReturn

import click
import typer
from pydantic import SecretStr, ValidationError
from rich.markup import escape

from plato.cli.utils import console
from plato.cli.vault import main as vault_main
from plato.cli.vault.client import DEFAULT_CONSOLE_HINT, ENV_VAR, VaultConsoleError
from plato.cli.vault.mail_models import (
    CHECK_EXIT,
    MailboxCreate,
    MailboxList,
    MailboxSetResult,
    MailCheckResult,
    MailCheckStatus,
    MailSetReport,
    WriteOutcome,
    mail_item_name,
    normalize_app_password,
    slugify,
)
from plato.cli.vault.main import ConsoleUrlArg, JsonArg, _fail, _field, _print_json

# The host the console reads these inboxes from (expd login_messages._IMAP_HOST).
IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993
IMAP_TIMEOUT_S = 20.0
# Swapped for a fake in the tests. Must take (host, port, ssl_context=..., timeout=...).
IMAP_SSL: Any = imaplib.IMAP4_SSL

mail_app = typer.Typer(
    help="Recovery inboxes: the mail-<account> items that email 2FA, the inbox page and the messages "
    "panel read. Through the login console only.",
    # Frame locals hold the app password: never print them in a traceback.
    pretty_exceptions_show_locals=False,
)


class MailUsageError(VaultConsoleError):
    """A bad option or a missing confirmation. Nothing was sent."""

    exit_code = 2


MailViaArg = Annotated[
    str,
    typer.Option(
        "--via",
        help="console only: the login console writes the 1Password item. Chronos has no mail-* route",
    ),
]
AddressArg = Annotated[
    str,
    typer.Option(
        "--address",
        help="The IMAP login: the real Gmail or Workspace mailbox, like jim@plato.so. A catch-all alias "
        "(x@bobwitmiester.com) is not a mailbox and fails the IMAP sign-in",
    ),
]
YesArg = Annotated[bool, typer.Option("--yes", "-y", help="Write without a question. Required without a TTY")]


def _stop(error: VaultConsoleError, json_output: bool) -> NoReturn:
    _fail(error, json_output)
    raise AssertionError("unreachable")


def _require_console(via: str, json_output: bool) -> None:
    if via != "console":
        _stop(
            MailUsageError(
                f"--via {via}: the mail-* items are served only by the login console. "
                "Chronos has no mail route. Use --via console (the default)"
            ),
            json_output,
        )


def _redact(text: str, secret: str | None) -> str:
    """An error text from the console or the IMAP server, with the password taken out.
    The console's 502 quotes the 1Password exception, and that text is not ours."""
    if secret:
        text = text.replace(secret, "***")
    return text


def _stdin_is_tty() -> bool:
    """A function, so a test can say "this is a terminal" (CliRunner stdin is never one)."""
    try:
        return sys.stdin.isatty()
    except (AttributeError, ValueError):
        return False


def _read_password(json_output: bool) -> str:
    """stdin when it is a pipe, else a hidden prompt. Gmail's spaces are removed."""
    if _stdin_is_tty():
        raw = typer.prompt("App password (input hidden)", hide_input=True, err=True)
    else:
        raw = typer.get_text_stream("stdin").read()
    if len([line for line in raw.splitlines() if line.strip()]) > 1:
        # All whitespace goes (Gmail's spaces), so two pasted lines would join into one wrong password,
        # and `--no-check` would write it.
        _stop(MailUsageError("stdin has more than one line: give only the app password"), json_output)
    password = normalize_app_password(raw)
    if not password:
        _stop(MailUsageError("no app password: pipe it on stdin, or run in a terminal for the prompt"), json_output)
    if not password.isascii():
        # imaplib sends LOGIN in ASCII: here and in every reader, a non-ASCII password raises
        # UnicodeEncodeError, not an IMAP refusal. The message does not quote the password.
        _stop(MailUsageError("the app password has a non-ASCII character: an IMAP login cannot send it"), json_output)
    if len(password) != 16:
        # Not refused: another provider's app password can have another length.
        typer.echo(f"warning: the password has {len(password)} characters. A Gmail app password has 16.", err=True)
    return password


def _model(account: str, address: str, password: str, json_output: bool) -> MailboxCreate:
    try:
        return MailboxCreate(account=account, email=address, password=SecretStr(password))
    except ValidationError as e:
        # include_input=False: pydantic's message never quotes the value, so the password cannot show.
        parts = [
            f"{'.'.join(str(p) for p in err['loc']) or 'value'}: {err['msg']}"
            for err in e.errors(include_url=False, include_context=False, include_input=False)
        ]
        _stop(MailUsageError(f"invalid {'; '.join(parts)}"), json_output)


@contextmanager
def _console_client(console_url: str | None, json_output: bool, secret: str | None = None) -> Iterator[Any]:
    try:
        base = console_url or os.environ.get(ENV_VAR)
        if not base:
            raise VaultConsoleError(
                f"{ENV_VAR} is not set. Point it at the login console backend, for example {DEFAULT_CONSOLE_HINT}"
            )
        with vault_main.VaultConsoleClient(base.rstrip("/")) as client:
            yield client
    except (click.exceptions.Exit, click.exceptions.Abort):
        raise
    except VaultConsoleError as e:
        err = type(e)(_redact(str(e), secret))
        _fail(err, json_output)
    except Exception as e:
        # A reply that is not the expected shape: its text is not shown (it can quote the input).
        _fail(vault_main._unexpected(e), json_output)


def run_check(account: str, address: str, password: str) -> MailCheckResult:
    """One IMAP sign-in and sign-out. No SELECT and no FETCH, so no mail is read or marked."""
    status, detail = MailCheckStatus.ok, None
    imap = None
    try:
        # A verifying context: with no ssl_context, IMAP4_SSL checks neither the CA nor the host name,
        # so any server on the path would get the app password in the LOGIN line.
        imap = IMAP_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ssl.create_default_context(), timeout=IMAP_TIMEOUT_S)
        imap.login(address, password)
    except ssl.SSLError as e:  # before OSError: SSLError is one
        status, detail = MailCheckStatus.tls_error, type(e).__name__
    except imaplib.IMAP4.abort as e:  # before IMAP4.error: abort is one (the link dropped)
        status, detail = MailCheckStatus.unreachable, _redact(str(e), password)
    except imaplib.IMAP4.error as e:
        status, detail = MailCheckStatus.auth_failed, _redact(_text(e), password)
    except OSError as e:
        status, detail = MailCheckStatus.unreachable, f"{type(e).__name__}: {_redact(str(e), password)}"
    finally:
        if imap is not None:
            try:
                imap.logout()
            except (imaplib.IMAP4.error, OSError):
                pass
    return MailCheckResult(account=slugify(account), address=address, status=status, detail=detail)


def _text(error: Exception) -> str:
    """imaplib raises with the server reply as bytes, e.g. b'[AUTHENTICATIONFAILED] Invalid credentials'."""
    arg = error.args[0] if error.args else ""
    return arg.decode("utf-8", "replace") if isinstance(arg, bytes) else str(arg)


def _print_check(result: MailCheckResult) -> None:
    colour = "green" if result.status == MailCheckStatus.ok else "red"
    console.print(f"[{colour}]{result.status}[/{colour}] IMAP sign-in as {escape(result.address)}")
    if result.detail:
        _field("server", result.detail)
    if result.status == MailCheckStatus.auth_failed:
        console.print(
            "  [dim]Use an app password (Google account > Security > App passwords), not the normal password. "
            "The address must be the real mailbox, not a catch-all alias.[/dim]"
        )


@mail_app.command("set")
def set_mailbox(
    account: Annotated[str, typer.Argument(help="The account slug, e.g. jim. The item is mail-<account>")],
    address: AddressArg,
    no_check: Annotated[
        bool, typer.Option("--no-check", help="Write without the IMAP sign-in test first (not recommended)")
    ] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print the item name and address. Send nothing")] = False,
    yes: YesArg = False,
    via: MailViaArg = "console",
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Add or replace a recovery inbox. The app password comes on stdin or from a hidden prompt.

    The username field is the IMAP login, so --address must be the real mailbox. For persona addresses on a
    catch-all domain (<name>@bobwitmiester.com), give the one Workspace mailbox that receives them.
    """
    _require_console(via, json_output)
    item = mail_item_name(account)
    # Validated with a placeholder, so a bad account or address stops before the password is asked.
    planned = _model(account, address, "x", json_output)
    if dry_run:
        report = MailSetReport(account=planned.account, item=item, address=planned.email, outcome=WriteOutcome.dry_run)
        if json_output:
            _print_json(report.model_dump(mode="json"))
        else:
            console.print(
                f"dry run: would write {escape(item)} (username {escape(planned.email)}, password from stdin or a prompt)"
            )
        return
    tty = _stdin_is_tty()
    if not tty and not yes:
        _stop(MailUsageError("no terminal to confirm in: re-run with --yes, or --dry-run to see the plan"), json_output)

    password = _read_password(json_output)
    body = _model(account, address, password, json_output)
    check: MailCheckStatus | None = None
    if not no_check:
        result = run_check(body.account, body.email, password)
        check = result.status
        if result.status != MailCheckStatus.ok:
            if json_output:
                _print_json({"error": "the IMAP check did not pass, nothing written", **result.model_dump(mode="json")})
                raise typer.Exit(CHECK_EXIT[result.status])
            _print_check(result)
            console.print("[red]nothing written.[/red] Fix the password or address, or pass --no-check.")
            raise typer.Exit(CHECK_EXIT[result.status])
        if not json_output:
            _print_check(result)

    with _console_client(console_url, json_output, secret=password) as client:
        existing = MailboxList.model_validate(client.list_mailboxes()).mailboxes.get(slugify(account))
        if existing is not None:
            typer.echo(f"warning: {item} exists (username {existing}). This write replaces it.", err=True)
        if tty and not yes and not typer.confirm(f"Write {item} with username {body.email}?", err=True):
            _stop(MailUsageError("not confirmed: nothing written"), json_output)
        answer = MailboxSetResult.model_validate(client.add_mailbox(body))

    report = MailSetReport(
        account=body.account,
        item=answer.item,
        address=body.email,
        outcome=WriteOutcome.created if answer.created else WriteOutcome.updated,
        replaced_address=existing,
        check=check,
    )
    if json_output:
        _print_json(report.model_dump(mode="json"))
        return
    console.print(f"[green]{report.outcome}[/green] {escape(report.item)} (username {escape(report.address)})")


@mail_app.command("list")
def list_mailboxes(
    via: MailViaArg = "console",
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """List the recovery inboxes: account and address. Never a password.

    The console lists only items with both fields set, and it lists none when it cannot read 1Password."""
    _require_console(via, json_output)
    with _console_client(console_url, json_output) as client:
        listing = MailboxList.model_validate(client.list_mailboxes())
    if json_output:
        _print_json(dict(sorted(listing.mailboxes.items())))
        return
    views = listing.views()
    for view in views:
        console.print(f"{escape(view.item)}  {escape(view.address)}")
    console.print(f"[dim]{len(views)} inbox(es)[/dim]")


@mail_app.command("show")
def show_mailbox(
    account: Annotated[str, typer.Argument(help="The account slug, e.g. jim")],
    via: MailViaArg = "console",
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Show one recovery inbox: the item name and the address. Exit 4 when the account has no item."""
    _require_console(via, json_output)
    item = mail_item_name(account)
    with _console_client(console_url, json_output) as client:
        listing = MailboxList.model_validate(client.list_mailboxes())
    view = next((v for v in listing.views() if v.account == slugify(account)), None)
    if view is None:
        if json_output:
            _print_json({"account": slugify(account), "item": item, "address": None})
        else:
            console.print(f"no item: {escape(item)} is not listed")
        raise typer.Exit(4)
    if json_output:
        _print_json(view.model_dump(mode="json"))
        return
    console.print(f"[bold]{escape(view.item)}[/bold]")
    _field("address", view.address)


@mail_app.command("check")
def check_mailbox(
    account: Annotated[str, typer.Argument(help="The account slug, e.g. jim")],
    address: AddressArg,
    json_output: JsonArg = False,
):
    """Test an app password with one IMAP sign-in (imap.gmail.com:993). Reads no mail and writes nothing.

    The password comes on stdin or from a hidden prompt. Exit 0 ok, 1 auth_failed, 2 unreachable, 6 tls_error.
    It tests the password you give, not the stored item."""
    body = _model(account, address, "x", json_output)
    password = _read_password(json_output)
    result = run_check(body.account, body.email, password)
    if json_output:
        _print_json(result.model_dump(mode="json"))
    else:
        _print_check(result)
    raise typer.Exit(CHECK_EXIT[result.status])
