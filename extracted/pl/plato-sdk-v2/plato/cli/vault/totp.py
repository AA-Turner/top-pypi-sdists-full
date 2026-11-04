"""`plato vault totp`: turn on authenticator-app 2FA (TOTP) at the vendor, and keep the seed
in the login vault.

Code checks that the browser is signed in as the vault item's username before anything starts.
The seed goes to the login vault (one Chronos PATCH of ``totp_seed``) as soon as a code was typed.
No model sees the seed or a code. Backup codes go to a local 600 file (the vault has no notes field).
``code`` is the only command that prints a code. No command prints a seed or a backup code.
"""

from __future__ import annotations

import errno
import fcntl
import hmac
import os
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from datetime import UTC, datetime
from typing import Annotated, Any, NoReturn, Protocol
from urllib.parse import urlparse

import typer
from pydantic import SecretStr
from rich.markup import escape

from plato.chronos.login_vault import SESSION_ID_ENV_VAR, LoginVault, normalize_key
from plato.cli.chronos.settings import get_settings
from plato.cli.utils import console
from plato.cli.vault import app_portal, pi_browser, sign_in, totp_code, totp_portal, totp_store
from plato.cli.vault import main as vault_main
from plato.cli.vault.app_models import ConsentBrowser
from plato.cli.vault.backends import chronos_errors
from plato.cli.vault.client import GateRefused, NotFound, VaultConsoleError
from plato.cli.vault.main import AccountArg, ApiKeyArg, ChronosUrlArg, JsonArg, _field
from plato.cli.vault.sign_in_models import OnEmailCode, SignInSecrets
from plato.cli.vault.totp_models import (
    TOTP_RECIPES,
    AccountMatch,
    BackupCodesRecord,
    CodeResult,
    PendingSeedFile,
    SignedInCheck,
    TotpCodeReport,
    TotpEnrollReport,
    TotpParams,
    TotpPlan,
    TotpRecipe,
    TotpVendor,
    VaultTotpState,
)

totp_app = typer.Typer(
    help="Authenticator-app 2FA (TOTP) per vault account: enroll turns it on at the vendor and saves the "
    "seed in the login vault; code prints the current code. Canva only.",
    # Frame locals hold the seed and codes: never print them in a traceback.
    pretty_exceptions_show_locals=False,
)

# Type a code only when it has at least this many seconds left; else wait for the next one.
CODE_MIN_LEFT_S = 8
# Code attempts when the vendor refuses a code (clock skew): the second uses the next period.
MAX_CODE_ATTEMPTS = 2
# After an email-code prompt (code cannot read the inbox), the command waits in the same
# TaskSpace while a person types it: one look every PERSON_POLL_S, PERSON_POLLS looks (10 min).
PERSON_POLL_S = 5.0
PERSON_POLLS = 120
# Agent runs per enroll: after code signed in at a prompt, the agent goes on from there.
MAX_AGENT_RUNS = 3

# Tests patch these.
_clock = time.time
_sleep = time.sleep


class TotpRefused(VaultConsoleError):
    """The command will not start: a seed is already there, a pending seed waits, the
    account is archived, or the vendor's parameters do not fit the vault. Exit 3."""

    exit_code = 3


class WrongAccount(TotpRefused):
    """The browser is not signed in as the vault account, or code cannot tell: the setup
    did not start and nothing changed at the vendor. Exit 3."""


class TotpCheckFailed(VaultConsoleError):
    """The vault does not hold the seed that was set up. Exit 8."""

    exit_code = 8


class SeedNotSaved(VaultConsoleError):
    """The vendor may have 2FA on, but the vault write failed: the seed is only in the
    pending file. Exit 9."""

    exit_code = 9


VendorArg = Annotated[TotpVendor, typer.Option("--vendor", help="The vendor of the account")]


class TotpVault(Protocol):
    def read(self, login_key: str, account: str) -> VaultTotpState: ...

    def save_seed(self, login_key: str, account: str, seed: SecretStr) -> None: ...

    def check_edit(self, state: VaultTotpState) -> None: ...

    def close(self) -> None: ...


class ChronosTotpVault:
    """The Chronos login vault: one read (with the secrets) and one PATCH of ``totp_seed``.
    A personal key may edit any account; an org-wide key only the accounts a run or an
    org-wide key created (see :mod:`plato.chronos.login_vault`)."""

    def __init__(self, api_key: str, base_url: str, session_id: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self._vault = LoginVault(api_key=api_key, base_url=self.base_url, session_id=session_id)

    def close(self) -> None:
        self._vault.close()

    def read(self, login_key: str, account: str) -> VaultTotpState:
        with chronos_errors(self.base_url):
            found = self._vault.get_account(login_key, account)
        if found is None:
            raise NotFound(f"no vault item for {normalize_key(login_key)}/{normalize_key(account)}")
        seed = found.totp_seed
        return VaultTotpState(
            login_key=found.login_key,
            account=found.account,
            archived=found.archived_at is not None,
            seed=SecretStr(seed) if seed else None,
            created_by=found.created_by,
            login_url=found.login_url,
            username=found.username,
            password=SecretStr(found.password) if found.password else None,
        )

    def check_edit(self, state: VaultTotpState) -> None:
        """Prove that this key may edit the item BEFORE the vendor turns 2FA on: one PATCH
        that sets ``login_url`` to the value it has. A 403 raises :class:`GateRefused`."""
        with chronos_errors(self.base_url):
            self._vault.update_account(state.login_key, state.account, login_url=state.login_url or "")

    def save_seed(self, login_key: str, account: str, seed: SecretStr) -> None:
        # One PATCH; the other fields stay. The reply holds the secrets: it is dropped.
        with chronos_errors(self.base_url):
            self._vault.update_account(login_key, account, totp_seed=seed.get_secret_value())


def _vault(chronos_url: str | None, api_key: str | None) -> TotpVault:
    key = api_key or os.environ.get("PLATO_API_KEY") or None
    if not key:
        raise VaultConsoleError("the Chronos login vault needs a Plato key: set PLATO_API_KEY or pass --api-key")
    url = (chronos_url or get_settings().chronos_url).rstrip("/")
    session_id = os.environ.get(SESSION_ID_ENV_VAR, "").strip() or None
    return ChronosTotpVault(key, url, session_id=session_id)


def _note(text: str, json_output: bool) -> None:
    """A progress line: stdout for people, stderr under --json so stdout stays one JSON object."""
    if json_output:
        print(text, file=sys.stderr, flush=True)
    else:
        console.print(escape(text))


@contextmanager
def _driver(
    tools: app_portal.PortalTools,
    recipe: TotpRecipe,
    login_key: str,
    account: str,
    browser: ConsentBrowser = ConsentBrowser.ego,
) -> Iterator[Any]:
    """One TaskSpace (or Pi browser) for the command. ``finish()`` runs once at the end;
    after a hand-off it leaves the window to the person."""
    if browser == ConsentBrowser.pi:
        # Only this account's saved login: a shared one held another person's Canva session.
        driver: Any = pi_browser.PiDriver(tools, login=pi_browser.login_slug(login_key, account))
    else:
        driver = app_portal.EgoDriver(tools)
    driver.open_space(totp_portal.space_name(recipe, login_key, account))
    ok = False
    try:
        yield driver
        ok = True
    finally:
        try:
            driver.finish()
        except VaultConsoleError:
            if ok:
                raise


def _page(driver: Any, recipe: TotpRecipe) -> Any:
    """The code-only setup steps for the driver's browser."""
    if isinstance(driver, pi_browser.PiDriver):
        return pi_browser.PiTotpPage(driver, recipe)
    return totp_portal.TotpPage(driver, recipe)


def _hand_off(driver: Any) -> None:
    """Give the TaskSpace to a person. If the hand-off call fails, the TaskSpace still
    stays open: ``finish()`` must never close a window that a person needs."""
    try:
        driver.hand_off()
    except VaultConsoleError:
        driver.handed_off = True


def _save_hint(login_key: str, account: str, pending: object) -> str:
    return f"Save it: plato vault edit {login_key} -a {account} --creds-stdin < {pending}. Then remove the file"


def _wait_for_person(
    driver: Any, page: Any, need: app_portal.NeedPerson, json_output: bool, inbox: str | None = None
) -> None:
    """An email-code prompt that code found no field for: hand the TaskSpace to a person
    and wait in it for the QR code. A second run would open a new TaskSpace and meet the
    same prompt. ``inbox``: the vault username, which the code went to."""
    _hand_off(driver)
    where = inbox if inbox and "@" in inbox else "the account's email inbox"
    _note(
        f"the vendor asks for the {need.reason} (sent to {where}): type it in {app_portal.person_hint(driver)}. "
        f"This command waits up to {PERSON_POLLS * PERSON_POLL_S / 60:.0f} min for the QR code.",
        json_output,
    )
    for _ in range(PERSON_POLLS):
        try:
            if page.key_ready():
                # Code takes the window back, so finish() closes it at the end. A failed
                # call leaves it with the person.
                reclaim = getattr(driver, "reclaim", None)
                if reclaim is not None:
                    reclaim()
                return
        except VaultConsoleError:
            raise need from None  # the TaskSpace is out of reach after the hand-off
        _sleep(PERSON_POLL_S)
    raise app_portal.NeedPerson(
        f"no QR code showed in TaskSpace {driver.space_id} within {PERSON_POLLS * PERSON_POLL_S / 60:.0f} min "
        f"after the {need.reason} prompt. Nothing was typed and nothing was saved",
        reason=need.reason,
    )


def _secrets(state: VaultTotpState) -> SignInSecrets:
    """The vault item's sign-in values, from the read that the command did anyway."""
    return SignInSecrets(username=state.username, password=state.password, totp_seed=state.seed)


def _sign_in(
    driver: Any,
    recipe: TotpRecipe,
    state: VaultTotpState,
    on_email_code: OnEmailCode,
    json_output: bool,
    done: Any = None,
    reauth: bool = False,
) -> sign_in.SignInReport:
    """``reauth``: the setup agent stopped at a prompt on the settings page (the vendor's
    re-sign-in before a 2FA change), so code may fill a password or a code there too.
    Elsewhere code fills only the sign-in pages."""
    return sign_in.sign_in(
        driver,
        sign_in.page_for(driver),
        recipe.sign_in,
        lambda: _secrets(state),
        where=f"{state.login_key}/{state.account}",
        on_email_code=on_email_code,
        note=lambda text: _note(text, json_output),
        done=done,
        reauth_paths=[urlparse(recipe.settings_url).path] if reauth else [],
    )


@contextmanager
def _enroll_lock(local: totp_store.TotpLocalStore, login_key: str, account: str) -> Iterator[None]:
    """One enroll per account at a time on this machine. Two runs would both pass the
    pending-seed check, both turn 2FA on, and the second seed would replace the first
    one in the pending file and in the vault while the vendor holds the other. The lock
    is an fcntl lock on ``<account>.lock`` (mode 600) next to the pending seed; the
    kernel drops it when the process ends, so a crash leaves no stale lock."""
    path = local.pending_seed_path(login_key, account).with_name(f"{normalize_key(account)}.lock")
    local._ensure_dir(path)
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        os.fchmod(fd, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as e:
            if e.errno not in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EACCES):
                raise
            raise TotpRefused(
                f"another `plato vault totp enroll` for {login_key}/{account} runs now (it holds {path}). "
                "Wait until it ends, then run the command again. Nothing ran"
            ) from None
        yield
    finally:
        os.close(fd)  # closing the descriptor releases the lock


def _same_seed(a: SecretStr, b: SecretStr) -> bool:
    return hmac.compare_digest(
        totp_code.normalize_seed(a.get_secret_value()).encode(), totp_code.normalize_seed(b.get_secret_value()).encode()
    )


def _plan(recipe: TotpRecipe, login_key: str, account: str, replace: bool, local: Any) -> TotpPlan:
    return TotpPlan(
        vendor=recipe.vendor,
        login_key=login_key,
        account=account,
        settings_url=recipe.settings_url,
        replace=replace,
        steps=[
            "read the vault item (refuse when it has a TOTP seed, unless --replace)",
            "check that this key may edit the vault item (a PATCH that sets login_url to its own value)",
            f"code: open {recipe.settings_url}; fill a sign-in prompt there from the vault item; then read the "
            "signed-in account's email from the page "
            f"(no email there: from {', '.join(u for u in recipe.account_urls if u != recipe.settings_url) or '-'}); "
            "stop, with nothing changed, unless it is the vault item's username (case-folded) and no other "
            "account email shows",
            f"agent: on {recipe.settings_url}, start the authenticator-app setup (stops at the QR code)",
            "a sign-in prompt during the setup (password, authenticator code): code fills it from the vault item; "
            "an email code: --on-email-code person hands the window to a person, stop ends the command",
            "code: before it reads the key, check the page again; another account email there stops the command "
            "(no code was typed, so 2FA is not on)",
            "code: show and read the setup key from the page (no model sees it)",
            f"code: type the current code ({recipe.digits} digits) and click '{recipe.confirm_button}'",
            "save the seed in the login vault (totp_seed) at once",
            "code: read the backup codes into the local store (mode 600), then finish the setup "
            "(no codes read: the TaskSpace goes to a person to copy them)",
            "check: the vault holds the seed, and a fresh code computes; then delete the pending seed file",
        ],
        backup_codes_store=str(local.backup_codes_path(login_key, account)),
        pending_seed_file=str(local.pending_seed_path(login_key, account)),
    )


def _sign_in_hint(driver: Any, expected: str | None) -> str:
    who = expected or "the vault account"
    if isinstance(driver, pi_browser.PiDriver) and driver.login:
        cfg = driver.config
        run = f"ssh {cfg.target} {cfg.launcher}"
        return (
            f"To sign in as {who} on the Pi: run `{run} --start --login {driver.login}`, sign in at "
            f"{cfg.novnc_url}, then run `{run} --stop --save-login --login {driver.login}`"
        )
    return f"Sign in to the vendor as {who} in {app_portal.person_hint(driver)}"


def _typed_note(report: sign_in.SignInReport) -> str:
    """For a refusal after the first sign-in: what code typed into the vendor's page."""
    return ", ".join(sign_in._FIELD.get(s, s.value) for s in report.filled)


def _check_signed_in(
    driver: Any, page: Any, recipe: TotpRecipe, state: VaultTotpState, signed_in: sign_in.SignInReport | None = None
) -> SignedInCheck:
    """Before any 2FA change: code reads the signed-in account's email from the vendor's
    pages and compares it with the vault item's username. Anything but a match raises
    :class:`WrongAccount`, and the Pi stop then keeps no login (the cookies are not this
    account's). A failed read on one page goes on to the next page. If no page showed an
    email and a read failed, the read's :class:`EmailReadFailed` stops the command: a failed
    read is never "no email". The caller has opened ``recipe.settings_url``; on a match
    the browser is back on it. ``signed_in``: what the sign-in before the check did, so a
    refusal after it says that code typed into the page."""
    current = recipe.settings_url
    found: list[str] = []
    shown_on: str | None = None
    failed: totp_portal.EmailReadFailed | None = None
    for url in recipe.account_urls:
        if url != current:
            driver.goto(url)
            current = url
        try:
            found = page.signed_in_emails()
        except totp_portal.EmailReadFailed as e:
            failed = e
            continue
        if found:
            shown_on = url
            break
    if not found and failed is not None:
        raise failed
    check = totp_portal.check_signed_in(found, state.username, recipe, shown_on)
    if check.result == AccountMatch.match:
        if current != recipe.settings_url:
            driver.goto(recipe.settings_url)
        return check
    _refuse_account(driver, check, recipe, state, before_setup=True, signed_in=signed_in)


def _recheck_signed_in(driver: Any, page: Any, recipe: TotpRecipe, state: VaultTotpState, json_output: bool) -> None:
    """The second look, after the agent (and a person, after a hand-off) had the window and
    before code reads the key or types a code. At a password prompt a person can sign out
    and sign in as someone else, and the first check does not see that. Another email on
    the page stops the command; no code went in, so 2FA is not on. No email here is only a
    note: the setup dialog may hide it, and the first check read it before the setup. A
    failed read is not "no email": its :class:`EmailReadFailed` stops the command."""
    check = totp_portal.check_signed_in(page.signed_in_emails(), state.username, recipe, recipe.settings_url)
    if check.result == AccountMatch.match:
        return
    if check.result == AccountMatch.unknown:
        _note("the setup page shows no account email now; the check before the setup matched", json_output)
        return
    _refuse_account(driver, check, recipe, state, before_setup=False)


def _refuse_account(
    driver: Any,
    check: SignedInCheck,
    recipe: TotpRecipe,
    state: VaultTotpState,
    before_setup: bool,
    signed_in: sign_in.SignInReport | None = None,
) -> NoReturn:
    """Raise :class:`WrongAccount` for a check that did not match. The Pi stop then keeps
    no login: the cookies are not this account's."""
    # A window still with a person (a failed reclaim) is never stopped by finish(), and the
    # next start saves it into THIS account's tar: take it back, so it stops unsaved.
    reclaim = getattr(driver, "reclaim", None)
    if reclaim is not None and getattr(driver, "handed_off", False):
        with suppress(VaultConsoleError):
            reclaim()
    discard = getattr(driver, "discard_login", None)
    if discard is not None:
        discard()
    where = f"{state.login_key}/{state.account}"
    hint = _sign_in_hint(driver, check.expected)
    # After the setup started, the vendor's setup dialog is open but no code went in.
    nothing = "Nothing was changed" if before_setup else "No code was typed, so 2FA is not on"
    if before_setup and signed_in is not None and signed_in.filled:
        # The sign-in before the gate typed vault values into the page: never say "nothing".
        nothing = (
            f"Code signed in first (it typed the {_typed_note(signed_in)} from {where} into the vendor's page), "
            "and changed nothing else"
        )
    if check.result == AccountMatch.no_vault_email:
        ran = "Nothing ran" if signed_in is None or not signed_in.filled else nothing
        raise WrongAccount(
            f"the vault item {where} has no email as its username ({state.username or 'none'}), so code cannot "
            f"check which account the browser is signed in as. {ran}. Set it: "
            f"plato vault edit {state.login_key} -a {state.account} --username <email>"
        )
    if check.result == AccountMatch.unknown:
        raise WrongAccount(
            f"no signed-in account email showed on {', '.join(recipe.account_urls)}: the browser may not be signed "
            f"in. {nothing}. {hint}, then run the command again"
        )
    others = ", ".join(e for e in check.found if e != check.expected)
    if check.result == AccountMatch.ambiguous:
        raise WrongAccount(
            f"{check.page} shows {check.expected} and also {others}, so code cannot tell which account is signed "
            f"in. {nothing}"
        )
    # The saved login of this account may hold the other session, and the next start restores it again.
    raise WrongAccount(
        f"the browser is signed in as {others} ({check.page}), not as {check.expected}, the username of {where}. "
        f"{nothing}. Sign out of {others} first. {hint}, then run the command again"
    )


def _run_setup_agent(
    driver: Any,
    page: Any,
    recipe: TotpRecipe,
    state: VaultTotpState,
    on_email_code: OnEmailCode,
    json_output: bool,
) -> None:
    """Run the setup agent until the QR code step shows. At a sign-in prompt (the agent
    stops there and types nothing), code fills it from the vault item and the agent goes
    on. Only an email code goes to a person (``--on-email-code person``); a sign-in prompt
    that code finds no field for stops the command."""
    goal = totp_portal.agent_goal(recipe, driver.space_id, app_portal.driver_browser(driver))
    for _ in range(MAX_AGENT_RUNS):
        try:
            if isinstance(driver, pi_browser.PiDriver):
                # A Pi frame is a picture, and the QR code in it is the seed: no frame goes to
                # the agent once the page shows the setup key (the screen stays sealed).
                end = driver.agent(goal, secret_visible=page.key_ready, hand_off_on_need=False)
            else:
                end = driver.agent(goal, hand_off_on_need=False)
        except app_portal.NeedPerson as need:
            if need.reason not in sign_in.SIGN_IN_REASONS:
                _hand_off(driver)
                raise
            # The step comes from the fields on the page, not from the agent's reason. The
            # setup's own code input shows only after the QR code: done() stops before it.
            report = _sign_in(driver, recipe, state, on_email_code, json_output, done=page.key_ready, reauth=True)
            if page.key_ready():
                return
            if report.acted:
                continue  # signed in: the agent goes on from the page it is on now
            # Code found no field to fill. Only an email code may go to a person
            # (--on-email-code person); a password or an authenticator code never does.
            if need.reason != "email_code":
                raise sign_in.SignInFailed(
                    f"the setup agent stopped at a sign-in prompt ({need.reason}), but code found no sign-in field "
                    "there to fill from the vault item. Nothing was typed into the setup"
                    f"{app_portal.log_hint(driver.last_agent_log)}"
                ) from None
            if on_email_code == OnEmailCode.stop:
                raise sign_in.EmailCodeNeeded(
                    "the setup agent stopped at an email code, and --on-email-code stop was given: nothing was typed"
                    f"{app_portal.log_hint(driver.last_agent_log)}"
                ) from None
            _wait_for_person(driver, page, need, json_output, inbox=state.username)
            return
        if not end.ready_for_key:
            raise app_portal.PortalError(
                f"the setup agent did not reach the setup key: {end.reason or 'no reason given'}"
                f"{app_portal.log_hint(driver.last_agent_log)}"
            )
        return
    raise app_portal.PortalError(
        f"the setup agent stopped at a sign-in prompt {MAX_AGENT_RUNS} times; nothing was typed into the setup"
        f"{app_portal.log_hint(driver.last_agent_log)}"
    )


def _enroll_in_browser(
    driver: Any,
    recipe: TotpRecipe,
    vault: TotpVault,
    local: totp_store.TotpLocalStore,
    state: VaultTotpState,
    json_output: bool,
    on_email_code: OnEmailCode = OnEmailCode.person,
) -> TotpEnrollReport:
    login_key, account = state.login_key, state.account
    page = _page(driver, recipe)
    driver.goto(recipe.settings_url)
    # A browser with no session lands on the sign-in page: code signs in from the vault item.
    first = _sign_in(driver, recipe, state, on_email_code, json_output)
    if first.acted:
        driver.goto(recipe.settings_url)  # the vendor may land on its home page after a sign-in
    # The hard gate: no agent and no click before code knows whose account this is.
    signed_in = _check_signed_in(driver, page, recipe, state, first)
    _note(f"the browser is signed in as {signed_in.expected} (the vault item's username)", json_output)
    _run_setup_agent(driver, page, recipe, state, on_email_code, json_output)

    # The agent, and a person after a hand-off, had the window since the first check.
    _recheck_signed_in(driver, page, recipe, state, json_output)
    key, read = page.reveal_key()
    seed_len = len(key.seed.get_secret_value())
    if not key.params.vault_ok():
        raise TotpRefused(
            f"the vendor's TOTP uses {key.params.digits} digits, {key.params.period_s} s, {key.params.algorithm}; "
            "the login vault and the login world support only 6 digits, 30 s, SHA1. Nothing was typed"
        )
    pending = local.save_pending_seed(login_key, account, PendingSeedFile(totp_seed=key.seed))
    _note(
        f"read the setup key from the page ({key.source}, {seed_len} characters, "
        f"{read.uri_count or 0} URI(s), {read.key_count or 0} text key(s)). "
        f"A copy is in {pending} until the vault holds it.",
        json_output,
    )

    # The pending copy goes only when no code went into the page. Once a code is typed,
    # the vendor may have taken it (auto-submit, a late answer), so the seed must stay.
    result = CodeResult.unknown
    attempts = 0
    any_typed = False
    for attempt in range(MAX_CODE_ATTEMPTS):
        attempts += 1
        code, _ = totp_code.fresh_code(key.seed, key.params, min_left_s=CODE_MIN_LEFT_S, clock=_clock, sleep=_sleep)
        typed = page.type_code(code)
        del code
        any_typed = any_typed or bool(typed.typed)
        if typed.result not in {r.value for r in CodeResult}:
            if not any_typed:
                local.drop_pending_seed(login_key, account)
                raise app_portal.PortalError(
                    f"code could not type the code ({typed.inputs or 0} input(s), {typed.error or typed.result}); "
                    "nothing was confirmed and nothing was saved"
                )
            result = CodeResult.unknown  # an earlier code went in: the vendor may have taken it
            break
        result = CodeResult(typed.result)
        if result != CodeResult.rejected:
            break
        if attempt + 1 < MAX_CODE_ATTEMPTS:
            _note("the page refused the code; trying the next code", json_output)
            _sleep(totp_code.seconds_left(_clock(), key.params.period_s) + 0.5)
    if result == CodeResult.rejected:
        _hand_off(driver)
        raise app_portal.PortalError(
            f"the page refused the code {attempts} time(s), so the seed is NOT in the vault. The authenticator app "
            f"is most likely not on. The seed stays in {pending} (mode 600) and TaskSpace {driver.space_id} stays "
            f"open. Check {recipe.settings_url}. If the authenticator app is on: "
            f"{_save_hint(login_key, account, pending)}. If it is off, remove the file"
        )

    # Save the seed FIRST: from here the vendor may ask for a code at every sign-in.
    try:
        vault.save_seed(login_key, account, key.seed)
    except VaultConsoleError as e:
        key_hint = ""
        if isinstance(e, GateRefused) and str(e).startswith("403"):
            key_hint = (
                " This key may not edit the item, so the same command with it fails too: "
                "set PLATO_API_KEY to your personal key first."
            )
        raise SeedNotSaved(
            f"the vault write failed ({e}). The vendor may have 2FA on now, and the seed is only in {pending} "
            f"(mode 600).{key_hint} {_save_hint(login_key, account, pending)}"
        ) from None
    if result == CodeResult.unknown:
        _note(
            "the page gave no clear answer to the code. The seed is saved because 2FA may be on: "
            f"check {recipe.settings_url}",
            json_output,
        )

    saved_codes = 0
    codes_path: str | None = None
    try:
        codes = page.read_backup_codes()
        if codes:
            record = BackupCodesRecord(
                vendor=recipe.vendor, login_key=login_key, account=account, codes=codes, saved_at=datetime.now(UTC)
            )
            codes_path = str(local.save_backup_codes(record))
            saved_codes = len(codes)
    except VaultConsoleError as e:
        _note(f"the backup codes were not saved ({e})", json_output)
    finished = False
    handed_off = False
    if saved_codes:
        try:
            finished = page.finish_setup()
        except VaultConsoleError as e:
            _note(f"the finish click failed ({e}); the seed is saved", json_output)
    else:
        # The vendor shows the codes one time: keep the window open for a person.
        _hand_off(driver)
        handed_off = True
        _note(
            f"no backup codes were saved. The setup window stays open in TaskSpace {driver.space_id}: "
            f"copy the codes by hand, then click '{recipe.finish_button}'. "
            f"If the window still asks for a code, `plato vault totp code {login_key} -a {account}` gives one",
            json_output,
        )

    try:
        check = _check(vault, login_key, account, key.seed)
    except VaultConsoleError as e:
        why = str(e) if isinstance(e, TotpCheckFailed) else f"the read-back check could not run ({e})"
        raise TotpCheckFailed(
            f"{why}. The vendor may have 2FA on, and the seed is still in {pending} (mode 600). "
            f"{_save_hint(login_key, account, pending)}"
        ) from None
    local.drop_pending_seed(login_key, account)
    return TotpEnrollReport(
        vendor=recipe.vendor,
        login_key=login_key,
        account=account,
        space_id=driver.space_id,
        key_source=key.source,
        seed_len=seed_len,
        code_result=result,
        code_attempts=attempts,
        seed_saved=True,
        backup_codes_saved=saved_codes,
        backup_codes_path=codes_path,
        setup_finished=finished,
        handed_off=handed_off,
        check=check,
        signed_in_as=signed_in.expected or "",
    )


def _check(vault: TotpVault, login_key: str, account: str, seed: SecretStr) -> str:
    """Read the seed back from the vault, compare it, and compute a fresh code from it."""
    state = vault.read(login_key, account)
    if state.seed is None or not _same_seed(state.seed, seed):
        raise TotpCheckFailed(f"the vault item {login_key}/{account} does not hold the seed that was set up")
    code = totp_code.totp(state.seed, _clock())
    if len(code) != 6 or not code.isdigit():
        raise TotpCheckFailed("the vault's seed gives no 6-digit code")
    return "ok"


@totp_app.command("enroll")
def enroll(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. canva")],
    account: AccountArg,
    vendor: VendorArg = TotpVendor.canva,
    replace: Annotated[
        bool, typer.Option("--replace", help="Set up a new seed when the vault item already has one")
    ] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print the plan; runs nothing")] = False,
    yes: Annotated[
        bool, typer.Option("--yes", help="Required: runs a paid agent and changes the live account")
    ] = False,
    browser: Annotated[
        ConsentBrowser,
        typer.Option(
            "--browser", help="pi (the default): Chromium on pi5-2 (noVNC for a person); ego: ego-browser on this Mac"
        ),
    ] = ConsentBrowser.pi,
    on_email_code: sign_in.OnEmailCodeArg = OnEmailCode.person,
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """Turn on authenticator-app 2FA for the account at the vendor and save the seed in the
    login vault. An agent opens the setup; code reads the setup key, types the code and
    saves the seed, so no model sees the seed or a code. Backup codes go to
    ~/.plato-creds/vault-totp/ (mode 600). A sign-in prompt (email, password,
    authenticator code) is filled by code from the vault item. A code that the vendor
    sends by email needs a person (--on-email-code). Prints no seed, code or backup code."""
    with vault_main._errors(json_output):
        if browser == ConsentBrowser.none:
            raise VaultConsoleError("--browser none: `enroll` needs a browser (ego or pi)")
        recipe = TOTP_RECIPES[vendor]
        lk, ac = normalize_key(login_key), normalize_key(account)
        if not lk or not ac:
            raise VaultConsoleError("login_key and account must hold at least one letter or digit")
        local = totp_store.default_totp_store()
        plan = _plan(recipe, lk, ac, replace, local)
        if dry_run:
            if json_output:
                vault_main._print_json({"dry_run": True, "plan": plan.model_dump(mode="json")})
            else:
                console.print("[yellow]dry run - nothing ran[/yellow]")
                for key, value in plan.model_dump(mode="json", exclude={"steps"}).items():
                    _field(key, value)
                console.print("  [cyan]steps:[/cyan]")
                for n, step in enumerate(plan.steps, 1):
                    console.print(f"    {n}. {escape(step)}")
            return
        if not yes:
            raise VaultConsoleError(
                "refusing to run: `enroll` runs a paid browser agent and turns on 2FA at the live vendor account. "
                "Re-run with --yes, or --dry-run to see the plan."
            )
        # The lock comes BEFORE the pending-seed check and holds through the cleanup: a
        # second enroll for the account must not pass the check while the first one runs.
        with _enroll_lock(local, lk, ac):
            if local.has_pending_seed(lk, ac):
                path = local.pending_seed_path(lk, ac)
                raise TotpRefused(
                    f"{path} holds a seed from an earlier enroll that the vault may not have. If that setup turned "
                    f"2FA on, save it: plato vault edit {lk} -a {ac} --creds-stdin < {path}. Then remove the file"
                )
            vault = _vault(chronos_url, api_key)
            try:
                state = vault.read(lk, ac)
                if state.archived:
                    raise TotpRefused(f"{lk}/{ac} is archived: restore it first")
                if state.has_seed and not replace:
                    raise TotpRefused(
                        f"{lk}/{ac} already has a TOTP seed in the vault. Pass --replace to set up a new one "
                        "(turn the authenticator app off at the vendor first)"
                    )
                # The gate needs an email as the vault username. Judge that before the browser
                # opens: else the sign-in would type the password first, and the gate only after.
                no_email = totp_portal.check_signed_in([], state.username, recipe, None)
                if no_email.result == AccountMatch.no_vault_email:
                    raise WrongAccount(
                        f"the vault item {lk}/{ac} has no email as its username ({state.username or 'none'}), so "
                        "code cannot check which account the browser is signed in as. Nothing ran. Set it: "
                        f"plato vault edit {lk} -a {ac} --username <email>"
                    )
                # The seed write comes after the vendor turns 2FA on: prove the edit right first.
                try:
                    vault.check_edit(state)
                except GateRefused as e:
                    if not str(e).startswith("403"):
                        raise
                    raise TotpRefused(
                        f"this key may not edit {lk}/{ac} (created by {state.created_by or 'unknown'}), so the seed "
                        "could not be saved after the vendor turns 2FA on. An org-wide key may edit only the items "
                        "a run or an org-wide key made: set PLATO_API_KEY to your personal key. Nothing ran"
                    ) from None
                tools = app_portal.find_tools()
                if browser == ConsentBrowser.ego and tools.ego is None:
                    raise app_portal.PortalUnavailable("ego-browser is not installed here (or pass --browser pi)")
                if tools.agent is None:
                    raise app_portal.PortalUnavailable("no `claude` binary here for the setup agent")
                with _driver(tools, recipe, lk, ac, browser) as driver:
                    report = _enroll_in_browser(driver, recipe, vault, local, state, json_output, on_email_code)
                    notice = driver.notice
            finally:
                vault.close()
        if notice:
            _note("ego-browser says an update is available: run `ego-browser upgrade` when it suits you", json_output)
    if json_output:
        vault_main._print_json(report.model_dump(mode="json"))
        return
    console.print(f"[green]enrolled[/green] [bold]{escape(lk)}/{escape(ac)}[/bold] [dim]({report.vendor})[/dim]")
    _field("signed in as", report.signed_in_as)
    _field("key", f"{report.key_source}, {report.seed_len} characters")
    _field("code", f"{report.code_result} after {report.code_attempts} attempt(s)")
    _field("vault", "seed saved (totp_seed)")
    _field(
        "backup codes",
        f"{report.backup_codes_saved} in {report.backup_codes_path}" if report.backup_codes_path else "0",
    )
    _field("setup finished", "yes" if report.setup_finished else "no (check the settings page)")
    if report.handed_off:
        _field("taskspace", f"{report.space_id} stays open for a person")
    _field("check", report.check)


@totp_app.command("code")
def code_cmd(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. canva")],
    account: AccountArg,
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """Print the current 6-digit TOTP code from the vault's seed (6 digits, 30 s, SHA1).
    This command prints a secret ON PURPOSE: the code is its output. The code alone goes
    to stdout (so `$(plato vault totp code ...)` works) and its seconds left to stderr.
    The seed is never printed."""
    with vault_main._errors(json_output):
        lk, ac = normalize_key(login_key), normalize_key(account)
        vault = _vault(chronos_url, api_key)
        try:
            state = vault.read(lk, ac)
        finally:
            vault.close()
        if not state.has_seed:
            raise NotFound(f"{lk}/{ac} has no TOTP seed in the vault (run `plato vault totp enroll`)")
        assert state.seed is not None
        now = _clock()
        params = TotpParams()
        report = TotpCodeReport(
            login_key=lk,
            account=ac,
            code=totp_code.totp(state.seed, now, digits=params.digits, period_s=params.period_s),
            valid_for_s=totp_code.seconds_left(now, params.period_s),
        )
    if json_output:
        vault_main._print_json(report.model_dump(mode="json"))
        return
    print(report.code, flush=True)
    print(f"valid for {report.valid_for_s} s", file=sys.stderr, flush=True)
