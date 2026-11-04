"""Plato vault CLI - list, show, create, edit, bake, archive and restore login accounts.

The vault lives in Chronos (``/api/login-vault``: settings in its tables, secrets
in 1Password) and this CLI calls it with the Plato key it has (``PLATO_API_KEY``;
only Plato org keys get in). Inside a run (``SESSION_ID`` set) it also sends the
session id, so a change made with an org-wide key is recorded as that run's.
There is no fallback: a Chronos error is reported as it is. ``--via console``
uses the login console (``PLATO_VAULT_URL``) instead, on purpose only. See
``docs/exploration/vault-cli.md``.
"""

from __future__ import annotations

import json
import os
import traceback
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Annotated, Any, NoReturn, TypeVar

import click
import typer
from pydantic import BaseModel, ConfigDict, SecretStr, ValidationError
from rich.markup import escape
from rich.table import Table

from plato.chronos.login_vault import SESSION_ID_ENV_VAR, AccountStatus, LoginVault, archive_reason, normalize_key
from plato.cli.chronos.settings import get_settings
from plato.cli.utils import console
from plato.cli.vault.backends import (
    ARCHIVE_FIELDS,
    ChronosBackend,
    ChronosVaultMissing,
    ConsoleBackend,
    chronos_errors,
    default_for,
    is_archived,
)
from plato.cli.vault.client import (
    ENV_VAR,
    MODES,
    BakeOutcomeUnknown,
    ConsoleUnreachable,
    GateRefused,
    NotFound,
    PartialCreate,
    VaultConsoleClient,
    VaultConsoleError,
    quote_segment,
    translate_mode,
)
from plato.cli.vault.open_session import (
    DEFAULT_MINUTES,
    MAX_MINUTES,
    TERMINAL_STATUSES,
    OpenClient,
    build_open_launch,
    check_world_schema,
    clone_defaults,
    close_tags,
    count_last_bake,
    find_live_sessions,
    hosted_browser,
    max_sessions_of,
    needs_defaults,
    pick_account,
    refuse_if_busy,
    resolve_seed,
    wait_for_end,
    wait_for_link,
)

vault_app = typer.Typer(
    help="Login vault: list, show, create, edit, bake, archive and restore login accounts "
    "(the Chronos login vault; --via console for the login console).",
    # A traceback must never print frame locals here: they hold the revealed
    # secrets of --creds-stdin and the X-API-Key header (the main app does the same).
    pretty_exceptions_show_locals=False,
)

T = TypeVar("T")

VIA_CHOICES = ("chronos", "console")

ViaArg = Annotated[
    str,
    typer.Option(
        "--via",
        help="chronos: the Chronos login vault (the default); console: the login console's "
        "/api/logins routes instead. Never both: a Chronos error is reported, not retried elsewhere",
    ),
]
ChronosUrlArg = Annotated[
    str | None,
    typer.Option("--chronos-url", help="Chronos base URL (default: $CHRONOS_URL, else https://chronos.plato.so)"),
]
ApiKeyArg = Annotated[
    str | None,
    typer.Option("--api-key", help="Plato key for the Chronos vault (default: $PLATO_API_KEY)"),
]
ConsoleUrlArg = Annotated[
    str | None,
    typer.Option("--console-url", help=f"Login console base URL, for --via console (default: ${ENV_VAR})"),
]
JsonArg = Annotated[bool, typer.Option("--json", "-j", help="Output as JSON")]
AccountArg = Annotated[str, typer.Option("--account", "-a", help="Account under the login_key")]
ModeArg = Annotated[
    str | None,
    typer.Option("--mode", help=f"Browser mode: one of {', '.join(MODES)} (or the vault's own spelling)"),
]
LoginUrlArg = Annotated[str | None, typer.Option("--login-url", help='Sign-in page a bake opens ("" clears)')]
LoginHintArg = Annotated[str | None, typer.Option("--login-hint", help='This account\'s own sign-in note ("" clears)')]
ProxyExitArg = Annotated[
    str | None,
    typer.Option("--proxy-exit", help='Exit NAME the account signs in from, e.g. exit-1 ("" unbinds)'),
]
AutoRefreshArg = Annotated[
    bool | None,
    typer.Option(
        "--auto-refresh/--seed-only",
        help="--auto-refresh: runs re-bake a stale snapshot themselves; --seed-only: a human bakes, runs never re-bake",
    ),
]
StatusArg = Annotated[
    str | None,
    typer.Option(
        "--status",
        help="Whether the account exists on the site yet: not_started (made for a sign-up), in_progress, "
        'done ("" clears: an account made before the field). Chronos vault only',
    ),
]
MaxSessionsArg = Annotated[
    int | None,
    typer.Option(
        "--max-sessions",
        min=1,
        max=50,
        help="How many live sessions (opens, bakes, runs) may use the account at once; 1 = one at a time "
        "(the default). Chronos vault only",
    ),
]
CredsStdinArg = Annotated[
    bool,
    typer.Option(
        "--creds-stdin",
        help="Read secrets as one JSON object on stdin: username, password, totp_seed, phone, security_qa",
    ),
]


# --------------------------------------------------------------------------- #
# output helpers
# --------------------------------------------------------------------------- #


def _print_json(payload: Any) -> None:
    """One JSON object on stdout - use print() so Rich adds no ANSI codes."""
    print(json.dumps(payload, indent=2, default=str))


# Keys that print under another label (show / edit).
_LABELS = {"max_sessions": "max sessions"}


def _field(key: str, value: Any) -> None:
    """One `  key: value` line. The value is remote text (a proxy note, a hint,
    an exception string), so it is escaped - rich markup would eat `[agent]` and
    a stray closing tag would raise MarkupError mid-render. A list of names
    (``default_for``, ``method_kinds``) prints comma-separated, ``-`` when empty."""
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        value = ", ".join(value) or "-"
    console.print(f"  [cyan]{_LABELS.get(key, key)}:[/cyan] {escape(str(value))}")


def _fail(error: VaultConsoleError, json_output: bool, **extra: Any) -> NoReturn:
    if json_output:
        _print_json({"error": str(error), **extra})
    else:
        console.print(f"[red]{escape(str(error))}[/red]")
    raise typer.Exit(error.exit_code)


def _unexpected(error: Exception) -> VaultConsoleError:
    """Any other exception as a vault error that quotes nothing of it. Its text
    can carry a secret (pydantic quotes the input, a JSON error the reply), so
    only its type and where it was raised are shown."""
    if isinstance(error, VaultConsoleError):
        return error
    if isinstance(error, ValidationError):
        return VaultConsoleError(f"invalid field(s): {_invalid_fields(error)}")
    frames = traceback.extract_tb(error.__traceback__)
    where = f" at {os.path.basename(frames[-1].filename)}:{frames[-1].lineno}" if frames else ""
    return VaultConsoleError(
        f"unexpected {type(error).__name__}{where}; its message is not shown because it can hold a secret"
    )


@contextmanager
def _errors(json_output: bool) -> Iterator[None]:
    """Typed vault errors -> their documented exit codes; anything else -> exit 1
    without its text (see :func:`_unexpected`)."""
    try:
        yield
    except (click.exceptions.Exit, click.exceptions.Abort, click.ClickException):
        raise
    except VaultConsoleError as e:
        _fail(e, json_output)
    except Exception as e:
        _fail(_unexpected(e), json_output)


def _session_url(chronos_url: str, session_id: str) -> str:
    return f"{chronos_url.rstrip('/')}/sessions/{session_id}"


def _print_abort(session_id: str) -> None:
    console.print(
        f"to abort: plato chronos stop {escape(session_id)}  "
        "[dim](loses the snapshot - it commits only at the end of the run)[/dim]"
    )


def _print_watch(live: dict, session_url: str) -> None:
    """Watch links for an in-flight bake: noVNC for a VM bake, the session otherwise."""
    novnc = live.get("novnc") or []
    for entry in novnc:
        if isinstance(entry, dict) and entry.get("url"):
            # markup=False: the aliases are `agent`/`browser`, so rich would read
            # `[agent]` as a style tag and print the links unlabelled.
            console.print(f"  noVNC [{entry.get('alias')}]: {entry['url']}", markup=False)
    if not novnc:
        console.print(f"  session: {session_url}")
        if live.get("trajectory_only"):
            console.print("  [dim]no VM browser for this mode - watch the trajectory[/dim]")


def _refresh_cell(flag: Any) -> str:
    """The vault's auto_refresh flag as the policy it names. Absent renders "-",
    never "auto": default-on is the run's call, not a fact the source stated."""
    if flag is True:
        return "auto"
    if flag is False:
        return "seed-only"
    return "-"


def _snapshot_cell(snapshot: Any) -> str:
    if not isinstance(snapshot, dict) or not snapshot:
        return "-"
    status = snapshot.get("status") or "none"
    age = snapshot.get("age_days")
    return f"{status} {age}d" if age is not None else str(status)


def _is_default(row: dict) -> bool:
    """Whether this account is the default login for its own login_key: the one
    auto_login runs sign in with, and `plato vault open <login_key>` without -a opens."""
    return normalize_key(str(row.get("login_key") or "")) in (default_for(row) or [])


def _account_cell(row: dict) -> str:
    """The account, marked ``*`` when it is its app's default and ``(archived)``
    when it is archived. Marks in this cell, not columns of their own, so the
    table still fits 80 columns."""
    account = str(row.get("account") or "")
    if _is_default(row):
        account = f"{account} *"
    return f"{account} (archived)" if is_archived(row) else account


def _print_default_legend(rows: list[dict]) -> None:
    if any(_is_default(r) for r in rows):
        console.print(
            "* = the app's default account: auto_login runs sign in with it, and "
            "`plato vault open <login_key>` without -a opens it"
        )
    if any(is_archived(r) for r in rows):
        console.print("(archived) = a dead account: nothing may use it until `plato vault restore`")
    if any(default_for(r) is None for r in rows):
        console.print(
            "[dim]This vault does not say which account is the default, so `plato vault open` "
            "needs -a unless the app has only one account.[/dim]"
        )


def _print_incomplete(vault_error: str | None) -> None:
    """Say so when the list may be missing accounts: it is not the whole vault."""
    if vault_error:
        console.print(
            f"[red]This list may be incomplete: 1Password could not be listed ({escape(vault_error)}). "
            "Accounts made by hand in 1Password may be missing.[/red]"
        )


# --------------------------------------------------------------------------- #
# which vault
# --------------------------------------------------------------------------- #


class _Target:
    """Where a command's calls go: the Chronos vault (``--via chronos``, the
    default) or the login console (``--via console``). Only that one: a Chronos
    error, a missing route included, is reported as it is, never retried on the
    console.
    """

    def __init__(self, via: str, chronos_url: str | None, api_key: str | None, console_url: str | None) -> None:
        if via not in VIA_CHOICES:
            raise VaultConsoleError(f"--via must be one of {', '.join(VIA_CHOICES)}")
        self.via = via
        self.chronos_url = (chronos_url or get_settings().chronos_url).rstrip("/")
        self.api_key = api_key or os.environ.get("PLATO_API_KEY") or None
        # Inside a Chronos run: name the run (used by Chronos only for an org-wide key).
        self.session_id = os.environ.get(SESSION_ID_ENV_VAR, "").strip() or None
        self.console_url = console_url or os.environ.get(ENV_VAR) or None
        self.source: str | None = None

    def _backend(self) -> ChronosBackend | ConsoleBackend:
        if self.via == "console":
            if not self.console_url:
                raise VaultConsoleError(f"--via console needs the login console: set {ENV_VAR} or pass --console-url")
            return ConsoleBackend(self.console_url, client_factory=VaultConsoleClient)
        if not self.api_key:
            raise VaultConsoleError(
                "the Chronos login vault needs a Plato key: set PLATO_API_KEY or pass --api-key "
                "(or --via console for the login console)"
            )
        return ChronosBackend(self.api_key, self.chronos_url, session_id=self.session_id, vault_factory=LoginVault)

    def run(self, op: Callable[[Any], T]) -> T:
        backend = self._backend()
        try:
            result = op(backend)
            self.source = backend.name
            return result
        finally:
            backend.close()


# --------------------------------------------------------------------------- #
# secrets from stdin
# --------------------------------------------------------------------------- #

# Secrets are accepted only over stdin (`--creds-stdin`, one JSON object): a flag
# value lands in shell history and the process list. `totp` is the console's
# older name for `totp_seed`.
_STDIN_KEYS = frozenset({"username", "password", "totp_seed", "totp", "phone", "security_qa"})


class _QA(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str
    answer: SecretStr


class StdinCreds(BaseModel):
    """What `--creds-stdin` accepts. ``SecretStr`` fields print as ``**********``."""

    model_config = ConfigDict(extra="forbid")

    username: str | None = None
    password: SecretStr | None = None
    totp_seed: SecretStr | None = None
    phone: SecretStr | None = None
    security_qa: list[_QA] | None = None

    def to_fields(self) -> dict[str, Any]:
        """The vault fields, secrets revealed. Sent, never printed."""
        out: dict[str, Any] = {}
        if self.username is not None:
            out["username"] = self.username
        for key in ("password", "totp_seed", "phone"):
            value = getattr(self, key)
            if value is not None:
                out[key] = value.get_secret_value()
        if self.security_qa is not None:
            out["security_qa"] = [
                {"question": q.question, "answer": q.answer.get_secret_value()} for q in self.security_qa
            ]
        return out


def _invalid_fields(error: ValidationError) -> str:
    """The failing field paths only: pydantic's own message quotes the input. An
    unexpected key is user text (it could be a pasted secret), so its path stops
    at the parent and the key itself is never printed."""
    paths = set()
    for err in error.errors():
        loc = [str(p) for p in err["loc"]]
        if err["type"] == "extra_forbidden":
            loc = [*loc[:-1], "<unexpected key>"]
        paths.add(".".join(loc))
    return ", ".join(sorted(paths))


def read_stdin_creds(stdin_text: str, *, keep_clears: bool) -> dict[str, Any]:
    """Parse `--creds-stdin`. ``keep_clears`` (edit) keeps ``""``/``[]`` - they
    clear a field - while create drops them. Errors never quote the input."""
    try:
        raw = json.loads(stdin_text)
    except ValueError:
        raise VaultConsoleError("--creds-stdin expects one JSON object on stdin, and it did not parse") from None
    if not isinstance(raw, dict):
        raise VaultConsoleError("--creds-stdin expects one JSON object on stdin")
    unknown = set(raw) - _STDIN_KEYS
    if unknown:
        # Counted, not named: a key is user text and could be a pasted secret.
        raise VaultConsoleError(
            f"--creds-stdin: {len(unknown)} unknown key(s); accepted: {', '.join(sorted(_STDIN_KEYS - {'totp'}))}"
        )
    if "totp" in raw:
        if "totp_seed" in raw:
            raise VaultConsoleError("--creds-stdin: give totp_seed or totp, not both")
        raw["totp_seed"] = raw.pop("totp")
    empty = (None,) if keep_clears else (None, "", [])
    try:
        creds = StdinCreds.model_validate({k: v for k, v in raw.items() if v not in empty})
    except ValidationError as e:
        raise VaultConsoleError(f"--creds-stdin: invalid field(s): {_invalid_fields(e)}") from None
    return creds.to_fields()


def _presence(fields: dict[str, Any]) -> dict[str, bool]:
    """What may be shown about the secrets a request carries: presence only."""
    return {k: k in fields for k in ("password", "totp_seed", "phone", "security_qa")}


def _shown(fields: dict[str, Any]) -> dict[str, Any]:
    """A create/edit request as it may be printed: non-secret fields, presence for the rest."""
    shown = {k: v for k, v in fields.items() if k not in ("password", "totp_seed", "phone", "security_qa")}
    shown["secrets"] = _presence(fields)
    return shown


def _config_fields(
    *,
    username: str | None = None,
    login_email: str | None = None,
    mode: str | None = None,
    login_url: str | None = None,
    login_hint: str | None = None,
    proxy_exit: str | None = None,
    auto_refresh: bool | None = None,
    max_sessions: int | None = None,
    account_status: str | None = None,
) -> dict[str, Any]:
    """The non-secret flags as vault fields (None = not given)."""
    fields: dict[str, Any] = {}
    if account_status is not None:
        status = account_status.strip()
        if status and status not in {s.value for s in AccountStatus}:
            raise VaultConsoleError(
                f'--status must be one of {", ".join(s.value for s in AccountStatus)} (or "" to clear)'
            )
        fields["account_status"] = status
    if username is not None:
        fields["username"] = username
    if login_email is not None:
        fields["login_email"] = login_email.strip()
    if mode is not None:
        # "" clears the mode (Chronos only); anything else must be a known mode.
        fields["browser_mode"] = "" if mode == "" else translate_mode(mode)
    if login_url is not None:
        fields["login_url"] = login_url.strip()
    if login_hint is not None:
        fields["login_hint"] = login_hint.strip()
    if proxy_exit is not None:
        fields["proxy_exit"] = proxy_exit.strip()
    if auto_refresh is not None:
        fields["auto_refresh"] = auto_refresh
    if max_sessions is not None:
        fields["max_sessions"] = max_sessions
    return fields


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #


@vault_app.command("list")
def list_logins(
    login_key: Annotated[str | None, typer.Option("--login-key", help="Only this login_key")] = None,
    include_archived: Annotated[
        bool,
        typer.Option(
            "--archived",
            "--include-archived",
            help="Also list archived accounts, marked (archived)",
        ),
    ] = False,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """List the vault's accounts: which one is the app's default (*), browser mode,
    refresh policy, bound exit, last bake. Archived accounts only with --archived.
    `plato vault open <login_key>` without -a opens the default one."""
    with _errors(json_output):
        target = _Target(via, chronos_url, api_key, console_url)
        rows, vault_error = target.run(lambda b: b.list_accounts(login_key, include_archived))

    if json_output:
        # default_for: the app names this account is the default for; null when
        # the vault does not report defaults. vault_error: set when the list may
        # be incomplete.
        _print_json(
            {
                "source": target.source,
                "logins": [{**r, "default_for": default_for(r)} for r in rows],
                "vault_error": vault_error,
            }
        )
        return

    table = Table(title=f"Logins ({target.source})")
    for column in ("login_key", "account", "mode", "refresh", "exit", "snapshot", "last bake"):
        # Seven columns overflow an 80-col terminal; fold a long value onto a
        # second line rather than cutting it to "browse…" / "decod…".
        table.add_column(column, overflow="fold")
    for row in rows:
        last_bake = row.get("last_bake_at") or row.get("last_bake_session_id") or "-"
        # Every cell is remote text: escaped, or rich would read a `[...]` in a
        # key, account or exit name as a style tag.
        table.add_row(
            *(
                escape(str(cell))
                for cell in (
                    row.get("login_key"),
                    _account_cell(row),
                    row.get("browser_mode") or "-",
                    _refresh_cell(row.get("auto_refresh")),
                    # The BOUND exit. Absent renders "-", never "direct": a list
                    # cannot tell a direct account from an unreadable vault.
                    row.get("proxy_exit") or "-",
                    _snapshot_cell(row.get("snapshot")),
                    str(last_bake)[:19],
                )
            )
        )
    console.print(table)
    _print_default_legend(rows)
    _print_incomplete(vault_error)


def _app_settings_or_none(target: Any, login_key: str) -> Any:
    """The app's shared settings for `show` (Chronos only). None only when there are
    none to read: not Chronos, or a Chronos without the app route; any other error raises."""
    if target.via != "chronos" or not target.api_key:
        return None
    try:
        with (
            chronos_errors(target.chronos_url),
            LoginVault(api_key=target.api_key, base_url=target.chronos_url) as vault,
        ):
            return vault.get_app_settings(login_key)
    except (ChronosVaultMissing, NotFound):
        return None


def _show(
    login_key: str,
    account: str | None,
    via: str,
    chronos_url: str | None,
    api_key: str | None,
    console_url: str | None,
    json_output: bool,
) -> None:
    if account is None:
        with _errors(json_output):
            target = _Target(via, chronos_url, api_key, console_url)
            rows, vault_error = target.run(lambda b: b.list_accounts(login_key))
            if not rows and vault_error:
                # An incomplete list cannot say the key does not exist.
                raise ConsoleUnreachable(
                    f"no account listed for {login_key}, but the list may be incomplete: "
                    f"1Password could not be listed ({vault_error})"
                )
            if not rows:
                # The `--account` form 404s; an unknown key must not read as
                # "exists, no accounts" just because this form asks the list.
                raise NotFound(f"no such login_key: {login_key}")
            app = _app_settings_or_none(target, login_key)
        if json_output:
            accounts = [{"account": r.get("account"), "default_for": default_for(r)} for r in rows]
            _print_json(
                {
                    "source": target.source,
                    "login_key": login_key,
                    "app_settings": app.model_dump(mode="json") if app else None,
                    "accounts": accounts,
                    "vault_error": vault_error,
                }
            )
            return
        if app is not None:
            console.print(f"[bold]{escape(login_key)}[/bold] app-wide settings")
            _print_app_settings(app)
        console.print(
            f"[bold]{escape(login_key)}[/bold] accounts: " + (", ".join(escape(_account_cell(r)) for r in rows) or "-")
        )
        _print_default_legend(rows)
        _print_incomplete(vault_error)
        return

    with _errors(json_output):
        target = _Target(via, chronos_url, api_key, console_url)
        view = target.run(lambda b: b.show(login_key, account))

    if json_output:
        _print_json({**view, "default_for": default_for(view), "source": target.source})
        return
    mark = " *" if _is_default({**view, "login_key": view.get("login_key", login_key)}) else ""
    if is_archived(view):
        mark += " [yellow](archived)[/yellow]"
    console.print(
        f"[bold]{escape(str(view.get('login_key', login_key)))}/{escape(str(view.get('account', account)))}[/bold]"
        f"{mark} [dim]({target.source})[/dim]"
    )
    for key, value in view.items():
        if key in ("login_key", "account"):
            continue
        if key in ARCHIVE_FIELDS and value is None:
            continue  # not archived: no three "None" lines
        _field(key, value)
    if "max_sessions" not in view:
        # The vault's rule: no max-sessions field = 1. The console does not read
        # the field, so say where the number comes from.
        _field("max_sessions", "1 (the default; the login console does not read this field)")


@vault_app.command("show")
def show(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. google")],
    account: Annotated[str | None, typer.Option("--account", "-a", help="Account; omit to list accounts")] = None,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Show one account: its login config, bound exit, last bake, credential presence. Never values."""
    _show(login_key, account, via, chronos_url, api_key, console_url, json_output)


@vault_app.command("get", hidden=True)
def get(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. google")],
    account: Annotated[str | None, typer.Option("--account", "-a", help="Account; omit to list accounts")] = None,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """The old name of `show`."""
    _show(login_key, account, via, chronos_url, api_key, console_url, json_output)


def _explain_conflict(
    target: _Target, refused: GateRefused, login_key: str, account: str, json_output: bool
) -> NoReturn:
    """A create 409 is not proof the account is usable: it may have no login URL,
    and on the console the title may belong to ANOTHER pair. Look it up and say
    which. Exit 3 either way."""
    try:
        view: dict | None = target.run(lambda b: b.show(login_key, account))
    except VaultConsoleError:
        view = None
    exists = view is not None
    bakeable = bool(view.get("bakeable")) if view is not None else False
    archived = view is not None and is_archived(view)
    if not exists:
        hint = "the account was NOT created: another account's 1Password item has that title"
    elif archived:
        hint = (
            f"the account exists but is archived: `plato vault restore {login_key} -a {account}` "
            "only if it works again, or create the new account under another name"
        )
    elif bakeable:
        hint = "the account already exists and is bakeable: `plato vault bake` it"
    else:
        hint = "the account already exists but has no login URL: `plato vault edit --login-url`, then bake"
    if json_output:
        _print_json({"error": str(refused), "exists": exists, "archived": archived, "bakeable": bakeable, "next": hint})
    else:
        console.print(f"[red]{escape(str(refused))}[/red]")
        console.print(escape(hint))
    raise typer.Exit(refused.exit_code)


@vault_app.command()
def create(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. slack")],
    account: AccountArg,
    username: Annotated[str | None, typer.Option("--username", help="The sign-in name (not a secret)")] = None,
    email: Annotated[
        str | None,
        typer.Option(
            "--email",
            help="The login email: picks the inbox mail codes are read from. Also the username when none is given",
        ),
    ] = None,
    login_url: LoginUrlArg = None,
    mode: ModeArg = None,
    login_hint: LoginHintArg = None,
    proxy_exit: ProxyExitArg = None,
    auto_refresh: AutoRefreshArg = None,
    status: StatusArg = None,
    creds_stdin: CredsStdinArg = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print what would be created and exit")] = False,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Add an account to the vault. Signs up nothing: the account must already exist
    at the vendor. Follow with `bake` to sign in and save its snapshot."""
    with _errors(json_output):
        fields: dict[str, Any] = {}
        if creds_stdin:
            fields.update(read_stdin_creds(typer.get_text_stream("stdin").read(), keep_clears=False))
        flags = _config_fields(
            username=username or (email if not fields.get("username") else None),
            login_email=email,
            mode=mode,
            login_url=login_url,
            login_hint=login_hint,
            proxy_exit=proxy_exit,
            auto_refresh=auto_refresh,
            account_status=status,
        )
        if flags.get("browser_mode") == "":
            raise VaultConsoleError('--mode "" clears a mode; a new account has none to clear')
        fields.update(flags)
        if fields.get("password") and not fields.get("username"):
            raise VaultConsoleError("a password needs a username: pass --username/--email or put it on stdin")

    shown = {"login_key": login_key, "account": account, **_shown(fields)}
    if dry_run:
        if json_output:
            _print_json({"dry_run": True, "request": shown})
        else:
            console.print("[yellow]dry run - nothing created[/yellow]")
            for key, value in shown.items():
                _field(key, value)
        return

    with _errors(json_output):
        target = _Target(via, chronos_url, api_key, console_url)
        try:
            result = target.run(lambda b: b.create(login_key, account, fields))
        except GateRefused as refused:
            if not str(refused).startswith("409"):
                raise
            _explain_conflict(target, refused, login_key, account, json_output)

    view = result["view"]
    if json_output:
        _print_json({"source": target.source, "created": view, "partial": result["partial"]})
    else:
        console.print(f"[green]created[/green] {escape(login_key)}/{escape(account)} [dim]({target.source})[/dim]")
        for key, value in view.items():
            if key not in ("login_key", "account"):
                _field(key, value)
    if result["partial"]:
        error = PartialCreate(
            f"the console catalog row exists but {', '.join(result.get('failed') or [])} did not land; "
            "finish it with `plato vault edit` (re-running create is a 409)"
        )
        if not json_output:
            console.print(f"[red]{escape(str(error))}[/red]")
        raise typer.Exit(error.exit_code)


def _print_app_settings(settings: Any) -> None:
    for name in ("signup_allowed", "signup_url", "signup_hint", "login_hint"):
        value = getattr(settings, name, None)
        _field(name, ("yes" if value else "no") if name == "signup_allowed" else (value or "-"))


def _edit_app(
    login_key: str,
    fields: dict[str, Any],
    account_only: list[str],
    via: str,
    chronos_url: str | None,
    api_key: str | None,
    json_output: bool,
) -> None:
    """`edit` with no -a: the app's shared settings (the Chronos vault only)."""
    with _errors(json_output):
        if account_only:
            raise VaultConsoleError(f"{', '.join(account_only)} change one account: pass -a <account>")
        fields = {k: v for k, v in fields.items() if v is not None}
        if not fields:
            raise VaultConsoleError(
                "nothing to change: pass -a <account> with its fields, or app-wide "
                "--login-hint, --signup-url, --signup-hint and/or --signup-allowed"
            )
        target = _Target(via, chronos_url, api_key, None)
        if target.via != "chronos" or not target.api_key:
            raise VaultConsoleError("app-wide settings live in the Chronos vault: set PLATO_API_KEY (no --via console)")
        with (
            LoginVault(api_key=target.api_key, base_url=target.chronos_url) as vault,
            chronos_errors(target.chronos_url),
        ):
            settings = vault.update_app_settings(login_key, **fields)
    if json_output:
        _print_json({"app_wide": True, **settings.model_dump(mode="json")})
        return
    console.print(f"[bold]{escape(settings.login_key)}[/bold] app-wide settings (every account of the app)")
    _print_app_settings(settings)


@vault_app.command()
def edit(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. slack")],
    account: Annotated[
        str | None,
        typer.Option(
            "--account", "-a", help="The account to change; omit to change what every account of the app shares"
        ),
    ] = None,
    username: Annotated[str | None, typer.Option("--username", help='The sign-in name ("" clears)')] = None,
    email: Annotated[
        str | None,
        typer.Option("--email", help='The login email: picks the inbox mail codes are read from ("" clears)'),
    ] = None,
    mode: ModeArg = None,
    login_url: LoginUrlArg = None,
    login_hint: LoginHintArg = None,
    proxy_exit: ProxyExitArg = None,
    auto_refresh: AutoRefreshArg = None,
    max_sessions: MaxSessionsArg = None,
    status: StatusArg = None,
    signup_url: Annotated[
        str | None, typer.Option("--signup-url", help='App-wide (no -a): the site\'s sign-up page ("" clears)')
    ] = None,
    signup_hint: Annotated[
        str | None,
        typer.Option("--signup-hint", help='App-wide (no -a): sign-up steps every sign-up of the app gets ("" clears)'),
    ] = None,
    signup_allowed: Annotated[
        bool | None,
        typer.Option(
            "--signup-allowed/--no-signup-allowed",
            help="App-wide (no -a): let runs sign up new accounts on the app (a person's own key only)",
        ),
    ] = None,
    creds_stdin: CredsStdinArg = False,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Change some of an account's fields (-a), or with no -a what every account of
    the app shares (--login-hint, --signup-url, --signup-hint, --signup-allowed).
    Only the ones given change; "" clears one. Nothing is launched, so no
    confirmation: the next bake or run reads the new values.
    --max-sessions N lets N live sessions use the account at once (1 = the default).
    A personal key may edit any account. An org-wide key may edit only accounts an
    org-wide key or a run created (created_by run:* or org-key:*)."""
    app_wide = {"signup_url": signup_url, "signup_hint": signup_hint, "signup_allowed": signup_allowed}
    if account is None:
        account_only = {
            "--username": username,
            "--email": email,
            "--mode": mode,
            "--login-url": login_url,
            "--exit": proxy_exit,
            "--auto-refresh/--seed-only": auto_refresh,
            "--max-sessions": max_sessions,
            "--status": status,
            "--creds-stdin": creds_stdin or None,
        }
        _edit_app(
            login_key,
            {**app_wide, "login_hint": login_hint},
            [flag for flag, value in account_only.items() if value is not None],
            via,
            chronos_url,
            api_key,
            json_output,
        )
        return
    with _errors(json_output):
        if given := [f"--{k.replace('_', '-')}" for k, v in app_wide.items() if v is not None]:
            raise VaultConsoleError(f"{', '.join(given)} are app-wide: run it without -a")
        fields: dict[str, Any] = {}
        if creds_stdin:
            fields.update(read_stdin_creds(typer.get_text_stream("stdin").read(), keep_clears=True))
        # Translated before any request, so a bad mode makes no call.
        fields.update(
            _config_fields(
                username=username,
                login_email=email,
                mode=mode,
                login_url=login_url,
                login_hint=login_hint,
                proxy_exit=proxy_exit,
                auto_refresh=auto_refresh,
                max_sessions=max_sessions,
                account_status=status,
            )
        )
        if not fields:
            raise VaultConsoleError(
                "nothing to change: pass --mode, --login-url, --login-hint, --proxy-exit, "
                "--auto-refresh/--seed-only, --max-sessions, --status, --username, --email and/or --creds-stdin"
            )
        target = _Target(via, chronos_url, api_key, console_url)

    def apply(backend: Any) -> dict:
        result = backend.edit(login_key, account, fields)
        if result["view"] is None:
            # Several console writes: re-read so what prints is what the vault now
            # holds. The writes are in already, so a failed re-read only warns.
            try:
                result["view"] = backend.show(login_key, account)
            except VaultConsoleError as e:
                result["reread_error"] = str(e)
        return result

    try:
        result = target.run(apply)
    except Exception as raw:
        e = _unexpected(raw)
        applied = getattr(e, "applied", None) or []
        # Sent but unanswered (or answered with something unreadable), or failed in
        # an unexpected way: the change MAY be in.
        unsure = e is not raw or isinstance(e, ConsoleUnreachable)
        if json_output:
            _print_json({"error": str(e), "applied": applied, "may_have_landed": unsure and not applied})
        else:
            console.print(f"[red]{escape(str(e))}[/red]")
            if applied:
                console.print(f"[yellow]already applied before the failure:[/yellow] {escape(', '.join(applied))}")
            elif unsure:
                console.print(
                    f"[yellow]it may have landed: check with `plato vault show {escape(login_key)} "
                    f"--account {escape(account)}`[/yellow]"
                )
            else:
                console.print("[dim]nothing was applied[/dim]")
        raise typer.Exit(e.exit_code) from None

    view = result.get("view")
    if json_output:
        _print_json(
            {
                "source": target.source,
                "applied": result["applied"],
                "account": view,
                "reread_error": result.get("reread_error"),
            }
        )
        return
    console.print(
        f"[green]updated[/green] [bold]{escape(login_key)}/{escape(account)}[/bold] [dim]({target.source})[/dim]"
    )
    if view is None:
        console.print(f"[yellow]re-read failed:[/yellow] {escape(str(result.get('reread_error')))}")
        for key, value in _shown(fields).items():
            _field(key, value)
        return
    for key in ("browser_mode", "auto_refresh", "max_sessions", "login_url", "login_hint", "proxy_exit", "creds"):
        if key in view:
            _field(key, view.get(key))


@vault_app.command()
def bake(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. slack")],
    account: AccountArg,
    mode: Annotated[
        str | None,
        typer.Option("--mode", help=f"One of {', '.join(MODES)}; omit to use the saved mode"),
    ] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print the request and exit; launches nothing")] = False,
    yes: Annotated[bool, typer.Option("--yes", help="Required to actually launch")] = False,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Bake this account's snapshot. Launches a REAL session: it signs into the live
    account and costs money, so --yes is required. The vault (Chronos or the
    console) owns the rest: one bake per account at a time, the saved mode and exit.
    """
    if not dry_run and not yes:
        _fail(
            VaultConsoleError(
                "refusing to launch: `bake` signs into the live account and costs money. "
                "Re-run with --yes, or --dry-run to see the request."
            ),
            json_output,
        )

    with _errors(json_output):
        browser_mode = translate_mode(mode)
        target = _Target(via, chronos_url, api_key, console_url)

        if dry_run:
            # The read only feeds this display, so a launch never depends on a
            # second route answering.
            view = target.run(lambda b: b.show(login_key, account))
            path = (
                f"/api/login-vault/accounts/{quote_segment(login_key)}/{quote_segment(account)}/bake"
                if target.source == "chronos"
                else f"/api/logins/{quote_segment(login_key)}/{quote_segment(account)}/bake"
            )
            request = {
                "method": "POST",
                "source": target.source,
                "path": path,
                "browser_mode": browser_mode,
                "saved_browser_mode": view.get("browser_mode"),
                "bakeable": view.get("bakeable"),
                "proxy_exit": view.get("proxy_exit"),
                "snapshot": view.get("snapshot"),
            }
            if json_output:
                _print_json({"dry_run": True, "request": request})
            else:
                console.print("[yellow]dry run - nothing launched[/yellow]")
                for key, value in request.items():
                    _field(key, value)
            return

        result = target.run(lambda b: b.bake(login_key, account, browser_mode))
    session_id = str(result.get("session_id") or "")
    session_url = _session_url(target.chronos_url, session_id) if session_id else ""

    # The session is LIVE and billing from here. Print the id and the abort line
    # before anything that can fail: the watch links are decorative, but losing
    # the id leaves a paid session nobody can stop.
    if not json_output:
        console.print(
            f"[green]bake launched[/green] session {escape(session_id) or 'unknown'} [dim]({target.source})[/dim]"
        )
        if session_id:
            _print_abort(session_id)

    live: dict = {}
    live_error: str | None = None
    if session_id and target.source == "console":
        try:
            live = target.run(lambda b: b.status(login_key, account))
        except Exception as e:
            live_error = str(_unexpected(e))

    if json_output:
        _print_json(
            {
                "source": target.source,
                "session_id": session_id or None,
                "session_url": session_url or None,
                "browser_mode": result.get("browser_mode") or browser_mode,
                "live": live,
                "live_error": live_error,
            }
        )
        return

    if live_error:
        # A warning, never an exit code: the bake is running either way.
        console.print(f"[yellow]watch links unavailable:[/yellow] {escape(live_error)}")
    elif session_id:
        _print_watch(live, session_url)


@vault_app.command()
def status(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. slack")],
    account: AccountArg,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """This account's latest bake: the session to watch (Chronos), or the console's
    watch links for an in-flight bake."""
    with _errors(json_output):
        target = _Target(via, chronos_url, api_key, console_url)
        live = target.run(lambda b: b.status(login_key, account))

    if json_output:
        _print_json({**live, "source": target.source})
        return

    session_id = live.get("session_id")
    if not session_id:
        console.print(f"no bake for {escape(login_key)}/{escape(account)}")
        return
    session_url = _session_url(target.chronos_url, str(session_id))
    if target.source == "chronos":
        console.print(
            f"[bold]{escape(login_key)}/{escape(account)}[/bold] last bake: session {escape(str(session_id))} "
            f"({escape(str(live.get('last_bake_at') or '-'))})"
        )
        console.print(f"  session: {session_url}")
        return
    console.print(f"[bold]{escape(login_key)}/{escape(account)}[/bold] baking in session {escape(str(session_id))}")
    _print_watch(live, session_url)
    _print_abort(str(session_id))


@vault_app.command()
def archive(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. google")],
    account: AccountArg,
    reason: Annotated[
        str,
        typer.Option("--reason", help="Why it is dead, one line of at most 200 characters (required)"),
    ],
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Archive a dead account (say the vendor closed it). Nothing may use it until
    `plato vault restore`: the list hides it (see `list --archived`), and an open, a
    bake, an edit, a create of its name and a run that names it are refused. The
    1Password item stays. Any key of the vault org may: a person's, the
    org-wide key or a run's, for any account. Archiving it again changes nothing."""
    with _errors(json_output):
        # Checked before any request, so a bad reason makes no call.
        try:
            text = archive_reason(reason)
        except ValueError as e:
            raise VaultConsoleError(f"--reason: {e} (say why the account is dead)") from None
        target = _Target(via, chronos_url, api_key, console_url)
        row = target.run(lambda b: b.archive(login_key, account, text))
    _print_archive_result("archived", target, login_key, account, row, json_output)


@vault_app.command()
def restore(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. google")],
    account: AccountArg,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Restore an archived account, so it can be used again. Any key of the vault org
    may: a person's, the org-wide key or a run's. Restoring an account that is
    not archived changes nothing."""
    with _errors(json_output):
        target = _Target(via, chronos_url, api_key, console_url)
        row = target.run(lambda b: b.restore(login_key, account))
    _print_archive_result("restored", target, login_key, account, row, json_output)


def _print_archive_result(
    verb: str, target: _Target, login_key: str, account: str, row: dict, json_output: bool
) -> None:
    if json_output:
        _print_json({"source": target.source, verb: True, "account": row})
        return
    name = f"{escape(str(row.get('login_key') or login_key))}/{escape(str(row.get('account') or account))}"
    console.print(f"[green]{verb}[/green] [bold]{name}[/bold] [dim]({target.source})[/dim]")
    for key in ("archived_at", "archived_by", "archived_reason"):
        if row.get(key):
            _field(key, row[key])


# --------------------------------------------------------------------------- #
# open: a signed-in browser for a person
# --------------------------------------------------------------------------- #


def _busy_defaults(target: _Target, login_key: str, account: str) -> dict[str, list[tuple[str, str]]]:
    """The clone defaults the busy check needs for ``auto_login`` runs.

    Chronos rows name every clone each account is the default for. The console's
    list names only an account's own login_key, so this account's other clones
    (aliases such as ``gmail`` for google/alice) come from its ``show``. Another
    account's aliases stay unknown on the console. Archived accounts count too, as
    on the Chronos open route: a run started before the archive still uses one."""
    # An incomplete list only hides other accounts' aliases from this check.
    rows, _vault_error = target.run(lambda b: b.list_accounts(None, True))
    if all(isinstance(r.get("default_for"), list) for r in rows):
        return clone_defaults(rows)
    mine = {**target.run(lambda b: b.show(login_key, account)), "login_key": login_key, "account": account}
    others = [
        r
        for r in rows
        if (normalize_key(str(r.get("login_key") or "")), normalize_key(str(r.get("account") or "")))
        != (login_key, account)
    ]
    return clone_defaults([*others, mine])


def _open_plan(
    view: dict,
    *,
    reason: str,
    seed: Any,
    minutes: int,
    save: bool,
    opened_by: str,
) -> dict:
    """What `open` will do, as printed by --dry-run and the launch line."""
    return {
        "login_key": view.get("login_key"),
        "account": view.get("account"),
        "account_reason": reason,
        "browser": "browserbase (Live View)" if hosted_browser(view.get("browser_mode")) else "vm (noVNC)",
        "proxy_exit": view.get("proxy_exit"),
        "saved_login": seed.config_ref if seed else None,
        "minutes": minutes,
        "save": save,
        "opened_by": opened_by or None,
    }


@vault_app.command("open")
def open_browser(
    login_key: Annotated[str, typer.Argument(help="Which app login, e.g. yardi_breeze (see `plato vault list`)")],
    account: Annotated[
        str | None,
        typer.Option("--account", "-a", help="Account; omit for the app's default account"),
    ] = None,
    minutes: Annotated[
        int,
        typer.Option("--minutes", "-m", help=f"How long the browser stays open, 1..{MAX_MINUTES}"),
    ] = DEFAULT_MINUTES,
    save: Annotated[
        bool,
        typer.Option(
            "--save",
            help="When it ends, save the browser's login as the account's newest one "
            "(only if it is still signed in). Like a bake, refused "
            "while a bake or another saving open of the account is live",
        ),
    ] = False,
    wait: Annotated[
        bool,
        typer.Option("--wait/--no-wait", help="Wait for the browser link and print it (default), or return at launch"),
    ] = True,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print what would launch; launches nothing")] = False,
    world_package: Annotated[
        str | None, typer.Option("--world-package", hidden=True, help="Login world to launch (a dev build, say)")
    ] = None,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Open a real browser signed in to one of our app accounts, for a person.

    It loads the account's latest saved login first and signs in for real only if
    that login no longer works. Then it prints a link to the live browser (noVNC,
    or Browserbase Live View) and keeps the browser open for --minutes. End it
    early with `plato vault close <session>`. Nothing is saved unless --save (it
    saves only if an agent finds the browser still signed in at the end; VM and
    Browserbase alike). Refused while the account's live opens, bakes and runs reach its
    max sessions (1 unless set with `plato vault edit --max-sessions`); with
    --save, also while a bake or another saving open of it is live. Refused for
    an archived account, and for an app whose default account is archived
    (`plato vault restore` first). Costs money: it runs a VM and an agent.
    """
    with _errors(json_output):
        if not 1 <= minutes <= MAX_MINUTES:
            raise VaultConsoleError(f"--minutes must be 1..{MAX_MINUTES} (got {minutes})")
        target = _Target(via, chronos_url, api_key, console_url)
        if not target.api_key:
            raise VaultConsoleError(
                "`open` launches through Chronos with your own Plato key: set PLATO_API_KEY or pass --api-key"
            )
        # Archived accounts too: an archived default is refused by name, never
        # passed over for another account.
        rows, vault_error = target.run(lambda b: b.list_accounts(login_key, True))
        try:
            row, reason = pick_account(rows, login_key, account)
        except (NotFound, VaultConsoleError) as e:
            if not vault_error or isinstance(e, GateRefused):
                raise
            # The account (or the app's default) can be among the items the list missed.
            raise ConsoleUnreachable(
                f"{e}; the list may be incomplete: 1Password could not be listed ({vault_error})"
            ) from e
        view = {**row, "login_key": normalize_key(str(row.get("login_key") or login_key))}
        lk, ac = view["login_key"], normalize_key(str(view.get("account") or ""))
        view["account"] = ac
        login_url = str(view.get("login_url") or "").strip()
        if not login_url:
            raise VaultConsoleError(
                f"{lk}/{ac} has no login URL: set it with `plato vault edit {lk} -a {ac} --login-url <url>`"
            )
        base = target.chronos_url
        client = OpenClient(base, target.api_key)
        try:
            with chronos_errors(base):
                # What the open launches: Chronos's login settings, or nothing.
                settings = client.login_settings()
                package = world_package or settings.world.package
                # An older login world would run a real bake instead of opening.
                check_world_schema(client.world_schema(package), package)
                # The saved login comes first: a real sign-in only when it fails.
                seed = resolve_seed(base, target.api_key, lk, ac, view.get("browser_mode"))
                live = client.live_sessions()
                # An auto_login run signs in as its clone's default account,
                # which can be any app's: read them, but only when needed.
                defaults = _busy_defaults(target, lk, ac) if needs_defaults(live) else {}
                using = find_live_sessions(live, lk, ac, defaults)
                # The account's last bake counts while it has not ended, a
                # review status included (the Chronos open route's rule).
                using = count_last_bake(client.session, using, str(view.get("last_bake_session_id") or "") or None)
                # The console path has no max_sessions: 1, the vault's default.
                # --save rewrites the saved login, so it also keeps the bake's rule.
                refuse_if_busy(using, lk, ac, limit=max_sessions_of(view), save=save)
                opened_by = client.me()
            plan = _open_plan(view, reason=reason, seed=seed, minutes=minutes, save=save, opened_by=opened_by)
            plan.update(world=package, agent=settings.describe())
            body = build_open_launch(
                login_key=lk,
                account=ac,
                login_url=login_url,
                browser_mode=view.get("browser_mode"),
                proxy_exit=view.get("proxy_exit"),
                minutes=minutes,
                save=save,
                opened_by=opened_by,
                seed=seed,
                settings=settings,
                world_package=package,
            )
            if dry_run:
                if json_output:
                    _print_json({"dry_run": True, "source": target.source, "plan": plan, "launch": body})
                else:
                    console.print("[yellow]dry run - nothing launched[/yellow]")
                    for key, value in plan.items():
                        _field(key, value)
                return
            with chronos_errors(base, unknown=BakeOutcomeUnknown):
                session_id = client.launch(body)
            _open_after_launch(client, session_id, plan, base, wait=wait, json_output=json_output)
        finally:
            client.close()


def _open_after_launch(
    client: OpenClient, session_id: str, plan: dict, chronos_url: str, *, wait: bool, json_output: bool
) -> None:
    """Print the session the moment it exists, then (with --wait) the link."""
    session_url = _session_url(chronos_url, session_id) if session_id else ""
    if not json_output:
        # The session is live and billing from here: the id and the way to end it
        # come before anything that can fail.
        console.print(
            f"[green]opening[/green] {escape(str(plan['login_key']))}/{escape(str(plan['account']))} "
            f"({escape(str(plan['account_reason']))}) in session {escape(session_id or 'unknown')}"
        )
        console.print(f"  session: {session_url}")
        console.print(f"  to end it: plato vault close {escape(session_id)}")
        console.print(
            "  saved login: "
            + (escape(str(plan["saved_login"])) if plan["saved_login"] else "none - it will sign in for real")
        )
        console.print(f"  agent: {escape(str(plan['agent']))}")
    result: dict[str, Any] = {
        "session_id": session_id or None,
        "session_url": session_url or None,
        "plan": plan,
        "link": None,
        "status": None,
    }
    if not (wait and session_id):
        if json_output:
            _print_json(result)
        else:
            console.print("  the link will be on the session page")
        return
    if not json_output:
        console.print(
            "  [dim]waiting for the browser (sign-in can take a few minutes)... Ctrl-C stops waiting only[/dim]"
        )
    try:
        with chronos_errors(chronos_url):
            waited = wait_for_link(lambda: client.session(session_id))
    except KeyboardInterrupt:
        if json_output:
            _print_json(result)
        else:
            console.print("\nstopped waiting; the session keeps running. The link will be on the session page.")
        return
    except Exception as e:
        # The session is live and billing: whatever ends the wait, the caller
        # still gets its id, to watch it or end it with `plato vault close`.
        _fail(_unexpected(e), json_output, session_id=session_id, session_url=session_url, plan=plan)
    result.update(link=waited.link, status=waited.status, reason=waited.reason)
    # Ended without a link = it failed (exit 1). Still running after the wait =
    # not a failure: the link reaches the session page when it is ready.
    ended = waited.status in TERMINAL_STATUSES
    if json_output:
        _print_json(result)
        if not waited.link and ended:
            raise typer.Exit(VaultConsoleError.exit_code)
        return
    if not waited.link and not ended:
        console.print(
            "[yellow]no link yet[/yellow]: the session is still running; the link will be on the session page"
        )
        return
    if not waited.link:
        console.print(
            f"[red]no browser link[/red]: session {escape(waited.status or 'unknown')}"
            + (f" - {escape(str(waited.reason))}" if waited.reason else "")
        )
        raise typer.Exit(VaultConsoleError.exit_code)
    console.print(f"[bold green]browser ready:[/bold green] {escape(waited.link)}", soft_wrap=True)
    console.print(f"  open for {plan['minutes']} min; end it early with: plato vault close {escape(session_id)}")
    console.print("  [bold]do not change the password, 2FA, email or plan[/bold] - other runs share this account")


@vault_app.command("close")
def close_browser(
    session_id: Annotated[str, typer.Argument(help="The session `plato vault open` printed")],
    wait: Annotated[
        bool,
        typer.Option("--wait/--no-wait", help="Wait until the session has ended (default), or return at once"),
    ] = True,
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """End a `plato vault open` browser early, cleanly.

    It tags the session. Within 30 seconds the world sees the tag, closes the
    browser (a Browserbase browser is released) and ends the session. Use this,
    not `plato chronos stop`: a stop kills the VMs at once, so a Browserbase
    browser stays up, signed in, until it times out.
    """
    with _errors(json_output):
        target = _Target("chronos", chronos_url, api_key, None)
        if not target.api_key:
            raise VaultConsoleError("`close` needs your Plato key: set PLATO_API_KEY or pass --api-key")
        client = OpenClient(target.chronos_url, target.api_key)
        try:
            with chronos_errors(target.chronos_url):
                session = client.session(session_id)
                status = str(session.get("status") or "").lower()
                ended = status in TERMINAL_STATUSES
                if not ended:
                    tags = close_tags(session)
                    if tags is not None:  # None: already asked to close, nothing to write
                        client.set_tags(session_id, tags)
                    if wait:
                        status = wait_for_end(lambda: client.session(session_id))
        finally:
            client.close()
    done = status in TERMINAL_STATUSES
    if json_output:
        _print_json({"session_id": session_id, "status": status or None, "ended": done, "already_ended": ended})
        return
    if ended:
        console.print(f"session {escape(session_id)} already ended ({escape(status)})")
    elif done:
        console.print(f"[green]closed[/green] session {escape(session_id)} ({escape(status)})")
    elif wait:
        console.print(
            f"[yellow]asked to close[/yellow] session {escape(session_id)}; it is still {escape(status or 'running')}. "
            "It ends within 30 s of the browser being ready (a sign-in still running finishes first)"
        )
    else:
        console.print(f"asked to close session {escape(session_id)}; it ends within about 30 s")
