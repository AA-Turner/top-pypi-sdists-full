"""`plato vault personas` and `plato vault free`: the persona pool for sign-ups, in the Chronos login vault."""

from __future__ import annotations

import os
from typing import Annotated

import typer
from rich.markup import escape
from rich.table import Table

from plato.chronos.login_vault import SESSION_ID_ENV_VAR, LoginVault
from plato.chronos.models import LoginVaultFreePersona, LoginVaultPersona
from plato.cli.chronos.settings import get_settings
from plato.cli.utils import console
from plato.cli.vault import main as vault_main
from plato.cli.vault.backends import chronos_errors
from plato.cli.vault.client import VaultConsoleError
from plato.cli.vault.main import ApiKeyArg, ChronosUrlArg, JsonArg

personas_app = typer.Typer(
    help="The persona pool for sign-ups (email + phone per persona) in the Chronos login vault: list, show, set. "
    "`plato vault free --login-key <app>` picks the ones with no account on an app."
)

_STATE_TEXT = {
    "free": "free",
    "has_account": "has an account on {app}",
    "number_on_app": "number already on {app}",
    "number_deprecated": "number deprecated",
}


def _vault(chronos_url: str | None, api_key: str | None) -> tuple[LoginVault, str]:
    key = api_key or os.environ.get("PLATO_API_KEY") or None
    if not key:
        raise VaultConsoleError("the Chronos login vault needs a Plato key: set PLATO_API_KEY or pass --api-key")
    url = (chronos_url or get_settings().chronos_url).rstrip("/")
    session_id = os.environ.get(SESSION_ID_ENV_VAR, "").strip() or None
    return LoginVault(api_key=key, base_url=url, session_id=session_id), url


def _phone_cell(row: LoginVaultPersona | LoginVaultFreePersona) -> str:
    if not row.phone:
        return "-"
    status = row.phone_status.value if row.phone_status else "unknown"
    return row.phone if status == "active" else f"{row.phone} ({status})"


@personas_app.command("list")
def list_personas(
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """Every persona: email, the inbox its mail lands in, phone and the phone's status."""
    with vault_main._errors(json_output):
        vault, url = _vault(chronos_url, api_key)
        with vault, chronos_errors(url):
            personas = vault.list_personas().personas

    if json_output:
        vault_main._print_json({"personas": [p.model_dump(mode="json") for p in personas]})
        return
    table = Table(title="Personas")
    for column in ("persona", "email", "inbox", "phone"):
        table.add_column(column, overflow="fold")
    for p in personas:
        table.add_row(*(escape(cell) for cell in (p.persona, p.email, p.inbox or "-", _phone_cell(p))))
    console.print(table)


@personas_app.command("show")
def show_persona(
    persona: Annotated[str, typer.Argument(help="The persona's key, e.g. dana")],
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """One persona's whole record: email, inbox, phone, its fixture (name, gender, birth date, address, ...)
    and its accounts. What a sign-up types into a form about the person. Holds no secret: Chronos keeps only
    placeholders for a card, bank account or ID."""
    with vault_main._errors(json_output):
        vault, url = _vault(chronos_url, api_key)
        with vault, chronos_errors(url):
            row = vault.get_persona(persona)
        if row is None:
            raise VaultConsoleError(f"no persona {persona!r}: `plato vault personas list` shows them")

    if json_output:
        vault_main._print_json(row.model_dump(mode="json"))
        return
    console.print(f"[bold]{escape(row.persona)}[/bold]")
    vault_main._field("email", row.email)
    vault_main._field("inbox", row.inbox or "-")
    vault_main._field("phone", _phone_cell(row))
    vault_main._field("accounts", row.accounts)
    for name, value in row.fixture.model_dump(mode="json", exclude_none=True).items():
        if isinstance(value, dict):
            for key, item in value.items():
                vault_main._field(f"fixture.{name}.{key}", item)
        else:
            vault_main._field(f"fixture.{name}", value)


@personas_app.command("set")
def set_persona(
    persona: Annotated[str, typer.Argument(help="The persona's key, e.g. priya")],
    email: Annotated[str | None, typer.Option("--email", help="Its email (required for a new persona)")] = None,
    inbox: Annotated[
        str | None,
        typer.Option("--inbox", help='The 1Password mail item its mail lands in, e.g. mail-tom ("" clears)'),
    ] = None,
    phone: Annotated[
        str | None, typer.Option("--phone", help='Its phone number, from the TextVerified pool ("" clears)')
    ] = None,
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """Create a persona, or change some of its fields (only the ones given change). Chronos refuses an email
    another persona has (409) and a new phone whose number is deprecated."""
    with vault_main._errors(json_output):
        vault, url = _vault(chronos_url, api_key)
        with vault, chronos_errors(url):
            row = vault.set_persona(persona, email=email, inbox=inbox, phone=phone)

    if json_output:
        vault_main._print_json(row.model_dump(mode="json"))
        return
    console.print(f"[bold]{escape(row.persona)}[/bold]")
    vault_main._field("email", row.email)
    vault_main._field("inbox", row.inbox or "-")
    vault_main._field("phone", _phone_cell(row))


def free(
    login_key: Annotated[str, typer.Option("--login-key", help="The app to sign up on, e.g. canva")],
    show_all: Annotated[
        bool, typer.Option("--all", help="Every persona, with why it is not free (account, number in use, deprecated)")
    ] = False,
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """Personas with no account on the app yet, free ones first: sign up as one, then save the account with
    `plato vault create <app> --account <persona> --email <email> ...`. A persona is not free when it has an account on the app, its
    number is deprecated, or another account of the app has its number. Two runs may pick the same persona at
    once; the app refuses the second sign-up (email taken), so that run calls `free` again."""
    with vault_main._errors(json_output):
        vault, url = _vault(chronos_url, api_key)
        with vault, chronos_errors(url):
            answer = vault.free_personas(login_key, show_all=show_all)

    if json_output:
        vault_main._print_json(answer.model_dump(mode="json"))
        return
    if not answer.personas:
        console.print(f"[yellow]No free persona for {escape(answer.login_key)}[/yellow]")
        return
    table = Table(title=f"Personas for {answer.login_key}")
    columns = ("persona", "email", "phone", "state") if show_all else ("persona", "email", "phone")
    for column in columns:
        table.add_column(column, overflow="fold")
    for p in answer.personas:
        cells = [p.persona, p.email, _phone_cell(p)]
        if show_all:
            state = _STATE_TEXT[p.state.value].format(app=answer.login_key)
            cells.append(f"{state} ({', '.join(p.accounts)})" if p.accounts else state)
        table.add_row(*(escape(cell) for cell in cells))
    console.print(table)
