"""Never render the login detail or inventory payloads here: they carry credential fields."""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated, Any, NoReturn

import typer
from pydantic import ValidationError
from rich.markup import escape

from plato.cli.utils import console
from plato.cli.vault import main as vault_main
from plato.cli.vault.client import DEFAULT_CONSOLE_HINT, ENV_VAR, NotFound, VaultConsoleError
from plato.cli.vault.main import ConsoleUrlArg, JsonArg, _fail, _field, _print_json
from plato.personas.bind import bind_pack
from plato.personas.client import PersonaConsole
from plato.personas.fixture_pool import load_pool
from plato.personas.models import (
    BindReport,
    CheckProblem,
    PersonaCheckReport,
    PersonaCheckRow,
    PersonaMode,
    PersonaPack,
    PersonaRecord,
    PersonaUpdate,
    SourcedValue,
)


@contextmanager
def _console_client(console_url: str | None, json_output: bool) -> Iterator[Any]:
    """Persona records live only in the login console, so there is no ``--via``."""
    try:
        base = console_url or os.environ.get(ENV_VAR)
        if not base:
            raise VaultConsoleError(
                f"{ENV_VAR} is not set. Point it at the login console backend, for example {DEFAULT_CONSOLE_HINT}"
            )
        with vault_main.VaultConsoleClient(base.rstrip("/")) as client:
            yield client
    except VaultConsoleError as e:
        _fail(e, json_output)


persona_app = typer.Typer(help="Persona records: the one person behind each vault account, and walker binding.")


class PersonaUsageError(VaultConsoleError):
    """A bad combination of options. Nothing was sent."""

    exit_code = 2


def _stop(error: VaultConsoleError, json_output: bool) -> NoReturn:
    _fail(error, json_output)
    raise AssertionError("unreachable")


def _describe(error: Exception) -> str:
    """Never repeats the input (it may be a card number); an unknown key name shows as (unknown key)."""
    if isinstance(error, ValidationError):
        parts = []
        for e in error.errors(include_url=False, include_context=False, include_input=False):
            loc = [str(p) for p in e["loc"]]
            if e["type"] == "extra_forbidden" and loc:
                loc[-1] = "(unknown key)"
            parts.append(f"{'.'.join(loc) or 'value'}: {e['msg']}")
        return "; ".join(parts)
    return str(error)


def _print_record(record: PersonaRecord, json_output: bool) -> None:
    if json_output:
        _print_json(record.model_dump(mode="json"))
        return
    console.print(f"[bold]{escape(record.login_key)}/{escape(record.account)}[/bold]")
    _field("person_key", record.person_key)
    for name, value in record.live:
        if value is not None:
            src = value.source if value.value is not None else value.note
            _field(f"live.{name}", f"{value.value} ({src})")
    for name, value in record.fixture:
        if value is not None:
            _field(f"fixture.{name}", value)


@persona_app.command()
def show(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. slack")],
    account: Annotated[str, typer.Argument(help="Account under the login_key")],
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Show the account's persona record."""
    with _console_client(console_url, json_output) as client:
        record = PersonaConsole(client=client).get(login_key, account)
    if record is None:
        _stop(NotFound(f"no persona for {login_key}/{account}"), json_output)
    assert record is not None
    _print_record(record, json_output)


def _opt(name: str, help_text: str):
    return typer.Option(name, help=help_text)


@persona_app.command("set")
def set_persona(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. slack")],
    account: Annotated[str, typer.Argument(help="Account under the login_key")],
    person_key: Annotated[str | None, _opt("--person-key", "Links the accounts of one person, e.g. alice")] = None,
    name: Annotated[str | None, _opt("--name", "live name")] = None,
    display_name: Annotated[str | None, _opt("--display-name", "live display_name")] = None,
    first_name: Annotated[str | None, _opt("--first-name", "live first_name")] = None,
    last_name: Annotated[str | None, _opt("--last-name", "live last_name")] = None,
    email: Annotated[str | None, _opt("--email", "live email")] = None,
    phone: Annotated[str | None, _opt("--phone", "live phone")] = None,
    locale: Annotated[str | None, _opt("--locale", "live locale")] = None,
    timezone: Annotated[str | None, _opt("--timezone", "live timezone")] = None,
    job_title: Annotated[str | None, _opt("--job-title", "live job_title")] = None,
    company: Annotated[str | None, _opt("--company", "live company")] = None,
    avatar_asset: Annotated[str | None, _opt("--avatar-asset", "live avatar_asset")] = None,
    source: Annotated[
        str | None, _opt("--source", "Where the live values were read, e.g. 'app profile read 2026-10-12'")
    ] = None,
    note: Annotated[str | None, _opt("--note", "Note stored with each live value")] = None,
    json_file: Annotated[
        Path | None, _opt("--json-file", "A PersonaUpdate JSON (live and/or fixture); flags override its keys")
    ] = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Merge values into the account's persona record (one PUT). Omitted keys stay as they are."""
    flags = {
        "name": name,
        "display_name": display_name,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "locale": locale,
        "timezone": timezone,
        "job_title": job_title,
        "company": company,
        "avatar_asset": avatar_asset,
    }
    flags = {k: v for k, v in flags.items() if v is not None}
    if flags and not source:
        _stop(PersonaUsageError("--source is required: say where the value was read"), json_output)
    try:
        base = PersonaUpdate.model_validate_json(json_file.read_text()) if json_file else PersonaUpdate()
        data = base.model_dump(mode="json", exclude_unset=True)
        if person_key is not None:
            data["person_key"] = person_key
        if flags:
            live = dict(data.get("live") or {})
            for key, value in flags.items():
                sourced = SourcedValue(value=value, source=source, **({"note": note} if note else {}))
                live[key] = sourced.model_dump(mode="json", exclude_unset=True)
            data["live"] = live
        update = PersonaUpdate.model_validate(data)
    except (OSError, ValueError) as e:
        _stop(PersonaUsageError(f"bad persona values: {_describe(e)}"), json_output)
    if not update.model_fields_set:
        _stop(PersonaUsageError("nothing to set: give a live flag, --person-key or --json-file"), json_output)

    with _console_client(console_url, json_output) as client:
        record = PersonaConsole(client=client).put(login_key, account, update)
    _print_record(record, json_output)


@persona_app.command()
def bind(
    pack: Annotated[Path, typer.Option("--pack", help="The v3p pack JSON with persona_slots")],
    mode: Annotated[PersonaMode, typer.Option("--mode", help="live: one round from the console; sim: N rounds")],
    out: Annotated[Path, typer.Option("--out", help="Where to write the persona-values file")],
    login: Annotated[
        str | None, typer.Option("--login", help="live: the login the walk signs in as, e.g. canva/alice")
    ] = None,
    rounds: Annotated[int, typer.Option("--rounds", help="sim: number of rounds")] = 3,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Bind the pack's persona slots and write the walker's persona-values file (eval_walk --personas)."""
    try:
        raw = pack.read_bytes()
        persona_pack = PersonaPack.model_validate_json(raw)
    except (OSError, ValueError) as e:
        _stop(PersonaUsageError(f"cannot read pack {pack}: {_describe(e)}"), json_output)
    acting: PersonaRecord | None = None
    others: list[PersonaRecord] = []
    if mode == PersonaMode.live:
        if login is None or "/" not in login:
            _stop(PersonaUsageError("live mode needs --login KEY/ACCOUNT"), json_output)
        assert login is not None
        key, acct = login.split("/", 1)
        with _console_client(console_url, json_output) as client:
            personas = PersonaConsole(client=client)
            acting = personas.get(key, acct)
            if acting is None:
                _stop(NotFound(f"no persona for {key}/{acct}"), json_output)
            others = personas.others_with_persona(key, acct)
    try:
        result = bind_pack(persona_pack, raw, mode, rounds=rounds, acting=acting, others=others, pool=load_pool())
    except ValueError as e:
        _stop(VaultConsoleError(str(e)), json_output)
    out.write_text(result.values.model_dump_json(indent=1))
    report = BindReport(
        out=str(out),
        mode=mode,
        rounds=sorted(result.values.rounds),
        stories=len(persona_pack.persona_slots),
        gaps=result.gaps,
    )
    if json_output:
        _print_json(report.model_dump(mode="json"))
        return
    console.print(
        f"wrote {escape(report.out)}: mode {report.mode}, rounds {report.rounds}, "
        f"stories {report.stories}, gaps {len(report.gaps)}"
    )
    for gap in report.gaps:
        console.print(f"  gap {escape(gap.story_id)}/{escape(gap.slot)}/{escape(gap.field)}")


@persona_app.command()
def check(
    login_key: Annotated[str | None, typer.Option("--login-key", help="Only this login_key")] = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Check that every non-archived account has a persona with a name and an email. Exit 1 on any problem, and
    also when the account list may be incomplete (the console could not list 1Password)."""
    problems: list[PersonaCheckRow] = []
    checked = 0
    with _console_client(console_url, json_output) as client:
        personas = PersonaConsole(client=client)
        inventory = personas.inventory()
        vault_error = inventory.vault_error or None
        for group in inventory.groups:
            key = group.login_key
            if login_key and key.lower() != login_key.lower():
                continue
            for row in group.accounts:
                if row.archived:
                    continue
                acct = row.account
                checked += 1
                record = personas.get(key, acct) if row.has_persona else None
                if record is None:
                    problems.append(PersonaCheckRow(login_key=key, account=acct, problem=CheckProblem.no_persona))
                    continue
                if record.live.name is None or record.live.name.value is None:
                    problems.append(PersonaCheckRow(login_key=key, account=acct, problem=CheckProblem.no_name))
                if record.live.email is None or record.live.email.value is None:
                    problems.append(PersonaCheckRow(login_key=key, account=acct, problem=CheckProblem.no_email))
    incomplete = vault_error is not None
    report = PersonaCheckReport(
        ok=not problems and not incomplete,
        checked=checked,
        problems=problems,
        incomplete=incomplete,
        vault_error=vault_error,
    )
    if json_output:
        _print_json(report.model_dump(mode="json"))
    else:
        for p in problems:
            console.print(f"[red]{p.problem}[/red] {escape(p.login_key)}/{escape(p.account)}")
        status = "ok" if report.ok else f"{len(problems)} problems" + (", list incomplete" if incomplete else "")
        console.print(f"checked {checked} accounts: {status}")
        vault_main._print_incomplete(vault_error)
    if not report.ok:
        raise typer.Exit(1)
