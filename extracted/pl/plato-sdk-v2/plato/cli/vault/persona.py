"""Never render the login detail or inventory payloads here: they carry credential fields."""

from __future__ import annotations

import os
import re
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated, NoReturn

import typer
from pydantic import ValidationError
from rich.markup import escape

from plato.chronos.errors import ConflictError, UnprocessableEntityError
from plato.chronos.login_vault import SESSION_ID_ENV_VAR, LoginVault, normalize_key
from plato.chronos.models import LoginVaultAccountSummary, LoginVaultPersona, PersonaMismatch
from plato.cli.chronos.settings import get_settings
from plato.cli.utils import console
from plato.cli.vault import main as vault_main
from plato.cli.vault.backends import chronos_errors
from plato.cli.vault.client import NotFound, VaultConsoleError
from plato.cli.vault.main import ApiKeyArg, ChronosUrlArg, JsonArg, _fail, _field, _print_json
from plato.personas.bind import bind_pack
from plato.personas.client import PersonaVault
from plato.personas.fixture_pool import load_pool
from plato.personas.models import (
    BindReport,
    CheckProblem,
    PersonaCheckReport,
    PersonaCheckRow,
    PersonaFixAction,
    PersonaFixRow,
    PersonaMode,
    PersonaPack,
    PersonaRecord,
    PersonaUpdate,
    SourcedValue,
)


@contextmanager
def _personas(chronos_url: str | None, api_key: str | None, json_output: bool) -> Iterator[PersonaVault]:
    """Persona records live in the Chronos login vault (the one persona backend), so there is no ``--via``."""
    try:
        key = api_key or os.environ.get("PLATO_API_KEY") or None
        if not key:
            raise VaultConsoleError("the Chronos login vault needs a Plato key: set PLATO_API_KEY or pass --api-key")
        url = (chronos_url or get_settings().chronos_url).rstrip("/")
        session_id = os.environ.get(SESSION_ID_ENV_VAR, "").strip() or None
        with LoginVault(api_key=key, base_url=url, session_id=session_id) as vault, chronos_errors(url):
            yield PersonaVault(vault)
    except VaultConsoleError as e:
        _fail(e, json_output)
    except Exception as e:
        _fail(vault_main._unexpected(e), json_output)


persona_app = typer.Typer(
    help="Persona records in the Chronos login vault: the one person behind each vault account, and walker binding."
)


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
    if record.mismatch:
        console.print(
            f"[yellow]flagged:[/yellow] signs in with another {' and '.join(m.value for m in record.mismatch)} than its persona "
            "(linked anyway; `plato vault persona check --fix` relinks by email)"
        )


@persona_app.command()
def show(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. slack")],
    account: Annotated[str, typer.Argument(help="Account under the login_key")],
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """Show the account's persona record."""
    with _personas(chronos_url, api_key, json_output) as personas:
        record = personas.get(login_key, account)
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
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """Merge values into the account's persona record (one PUT). Omitted keys stay as they are. --person-key
    links the account to its persona (created when new, with the live email or the account's username); the
    fixture belongs to the persona, so every account of the person shares it."""
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

    with _personas(chronos_url, api_key, json_output) as personas:
        record = personas.put(login_key, account, update)
    _print_record(record, json_output)


@persona_app.command()
def bind(
    pack: Annotated[Path, typer.Option("--pack", help="The v3p pack JSON with persona_slots")],
    mode: Annotated[PersonaMode, typer.Option("--mode", help="live: one round from the vault; sim: N rounds")],
    out: Annotated[Path, typer.Option("--out", help="Where to write the persona-values file")],
    login: Annotated[
        str | None, typer.Option("--login", help="live: the login the walk signs in as, e.g. canva/alice")
    ] = None,
    rounds: Annotated[int, typer.Option("--rounds", help="sim: number of rounds")] = 3,
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
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
        with _personas(chronos_url, api_key, json_output) as personas:
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


# An account's username is its sign-in email when it looks like one (Chronos's persona link rule reads it the same way).
_SIGN_IN_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _fix_link(
    vault: LoginVault,
    row: LoginVaultAccountSummary,
    email: str,
    by_email: dict[str, LoginVaultPersona],
    by_key: dict[str, LoginVaultPersona],
    *,
    create: bool,
) -> tuple[PersonaFixRow, PersonaRecord] | None:
    """Link the account to the persona that has its sign-in email; with ``create``, make that persona
    (<login_key>_<account>) when none has it. Returns the fix and the record Chronos saved; None when nothing was
    changed (Chronos refused, or the key is taken)."""
    target = by_email.get(email)
    action = PersonaFixAction.relinked
    if target is None:
        if not create:
            return None
        key = normalize_key(f"{row.login_key}_{row.account}")
        if key in by_key:
            return None
        try:
            target = vault.set_persona(key, email=(row.username or "").strip())
        except (ConflictError, UnprocessableEntityError):
            return None
        by_key[target.persona] = by_email[email] = target
        action = PersonaFixAction.created
    try:
        linked = vault.set_account_persona(row.login_key, row.account, {"person_key": target.persona})
    except (ConflictError, UnprocessableEntityError):
        return None  # e.g. the account was archived meanwhile
    saved = PersonaRecord.model_validate(linked.model_dump(mode="json"))
    fix_row = PersonaFixRow(
        login_key=row.login_key, account=row.account, action=action, persona=target.persona, mismatch=saved.mismatch
    )
    return fix_row, saved


@persona_app.command()
def check(
    login_key: Annotated[str | None, typer.Option("--login-key", help="Only this login_key")] = None,
    fix: Annotated[
        bool,
        typer.Option(
            "--fix",
            help="Make each persona link follow the account's sign-in email: link it to the persona with that email, "
            "or make one from it when none has it. A phone that differs is only reported.",
        ),
    ] = False,
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """Check that every non-archived account has a persona with a name and an email, and that the account signs in
    with its persona's email and phone. Exit 1 on any problem left, and also when the account list may be incomplete
    (Chronos could not list 1Password)."""
    problems: list[PersonaCheckRow] = []
    fixed: list[PersonaFixRow] = []
    checked = 0
    with _personas(chronos_url, api_key, json_output) as personas:
        listing = personas.vault.list_accounts(login_key)
        vault_error = listing.vault_error or None
        records = {(r.login_key, r.account): r for r in personas.records(login_key)}
        pool = personas.vault.list_personas().personas
        by_key = {p.persona: p for p in pool}
        by_email = {p.email.lower(): p for p in pool}
        for row in listing.accounts:
            key, acct = row.login_key, row.account
            checked += 1
            record = records.get((key, acct))
            email = (row.username or "").strip().lower()
            fixable = fix and bool(_SIGN_IN_EMAIL.match(email))
            # No record, or a record linked to no persona: --fix links it to the persona with its sign-in email.
            if record is None or record.person_key is None:
                done = _fix_link(personas.vault, row, email, by_email, by_key, create=False) if fixable else None
                if done is None:
                    problems.append(PersonaCheckRow(login_key=key, account=acct, problem=CheckProblem.no_persona))
                    continue
                fixed.append(done[0])
                record = done[1]
            # Chronos flags each link whose account does not match its persona (`mismatch`); the link stands.
            if PersonaMismatch.email in record.mismatch:
                done = _fix_link(personas.vault, row, email, by_email, by_key, create=True) if fixable else None
                if done is not None:
                    fixed.append(done[0])
                    record = done[1]
                # Still flagged on the saved record (unfixed, or an edit landed before the link was saved).
                if PersonaMismatch.email in record.mismatch:
                    problems.append(PersonaCheckRow(login_key=key, account=acct, problem=CheckProblem.email_mismatch))
            # Read from the record Chronos saved last, so a fix that left a field empty is still reported.
            if record.live.name is None or record.live.name.value is None:
                problems.append(PersonaCheckRow(login_key=key, account=acct, problem=CheckProblem.no_name))
            if record.live.email is None or record.live.email.value is None:
                problems.append(PersonaCheckRow(login_key=key, account=acct, problem=CheckProblem.no_email))
            if PersonaMismatch.phone in record.mismatch:
                problems.append(PersonaCheckRow(login_key=key, account=acct, problem=CheckProblem.phone_mismatch))
    incomplete = vault_error is not None
    report = PersonaCheckReport(
        ok=not problems and not incomplete,
        checked=checked,
        problems=problems,
        fixed=fixed,
        incomplete=incomplete,
        vault_error=vault_error,
    )
    if json_output:
        _print_json(report.model_dump(mode="json"))
    else:
        for f in fixed:
            console.print(f"[green]{f.action}[/green] {escape(f.login_key)}/{escape(f.account)} -> {escape(f.persona)}")
        for p in problems:
            console.print(f"[red]{p.problem}[/red] {escape(p.login_key)}/{escape(p.account)}")
        status = "ok" if report.ok else f"{len(problems)} problems" + (", list incomplete" if incomplete else "")
        console.print(f"checked {checked} accounts: {status}" + (f", fixed {len(fixed)}" if fixed else ""))
        vault_main._print_incomplete(vault_error)
    if not report.ok:
        raise typer.Exit(1)
