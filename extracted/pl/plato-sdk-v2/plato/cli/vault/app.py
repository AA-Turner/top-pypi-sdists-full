"""`plato vault app`: a vendor OAuth app (client id, secret, refresh token) per vault account.

No command prints a secret. ``show`` prints presence, the first characters and the length of each value.
``token`` writes an access token to a 600 env file, and never the refresh token or the client secret.
"""

from __future__ import annotations

import base64
import getpass
import json
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any, cast
from urllib.parse import urlparse

import typer
from pydantic import SecretStr
from rich.markup import escape

from plato.chronos.login_vault import normalize_key
from plato.cli.utils import console
from plato.cli.vault import app_oauth, app_portal, app_store, pi_browser, sign_in, totp_portal
from plato.cli.vault import main as vault_main
from plato.cli.vault.app_models import (
    RECIPES,
    AppCredentials,
    AppVendor,
    ConsentBrowser,
    CredentialKind,
    CredentialSource,
    McpCheck,
    TokenFileReport,
    VendorRecipe,
    VendorUser,
)
from plato.cli.vault.client import NotFound, VaultConsoleError
from plato.cli.vault.main import AccountArg, ApiKeyArg, ChronosUrlArg, ConsoleUrlArg, JsonArg, ViaArg, _field
from plato.cli.vault.open_session import pick_account
from plato.cli.vault.sign_in_models import OnEmailCode, SignInSecrets
from plato.cli.vault.totp_models import AccountMatch

app_app = typer.Typer(
    help="Vendor OAuth apps per vault account (client id, secret, refresh token): create, import, "
    "consent, refresh, show, token. Phase 1: a local store on this machine; Canva only.",
    # Frame locals hold client secrets and tokens: never print them in a traceback.
    pretty_exceptions_show_locals=False,
)

_BROWSER_PLAN = {
    ConsentBrowser.ego: "ego-browser + agent",
    ConsentBrowser.pi: "Chromium on pi5-2 (CDP for code, the computer MCP over VNC for the agent)",
    ConsentBrowser.none: "none",
}
# `token` refreshes when the access token has less than this left.
TOKEN_MIN_LEFT_S = 300
# `create` and `consent` exit with this code when the grant serves mcp and the MCP
# check fails. The grant is stored first; `consent --kind mcp` checks it again.
MCP_CHECK_EXIT_CODE = 7


class AppUsageError(VaultConsoleError):
    """A bad combination of options. Nothing was sent or stored."""

    exit_code = 2


class WrongAppAccount(VaultConsoleError):
    """The browser is signed in as another vendor account than the record's: the consent
    page shows another email, or users/me names another user than the earlier grant.
    Nothing was stored. Exit 3."""

    exit_code = 3


VendorArg = Annotated[AppVendor, typer.Option("--vendor", help="The vendor of the app")]
KindArg = Annotated[
    str | None,
    typer.Option("--kind", help="What the grant serves, comma-separated: api (REST), mcp, or api,mcp"),
]
VaultCheckArg = Annotated[
    bool,
    typer.Option(
        "--vault-check/--no-vault-check",
        help="Check that the account exists in the login vault, and is not archived (needs PLATO_API_KEY)",
    ),
]
YesArg = Annotated[bool, typer.Option("--yes", help="Required to run the browser agent (it costs money)")]
PortalBrowserArg = Annotated[
    ConsentBrowser,
    typer.Option(
        "--browser",
        help="ego: ego-browser on this Mac; pi: Chromium on pi5-2, driven over ssh (a person takes over in noVNC)",
    ),
]


def _parse_kinds(raw: str | None, default: list[CredentialKind]) -> list[CredentialKind]:
    if raw is None:
        return list(default)
    kinds: list[CredentialKind] = []
    for part in (p.strip().lower() for p in raw.split(",")):
        if not part:
            continue
        try:
            kind = CredentialKind(part)
        except ValueError:
            raise AppUsageError(
                f"--kind: {part!r} is not one of {', '.join(k.value for k in CredentialKind)}"
            ) from None
        if kind not in kinds:
            kinds.append(kind)
    if not kinds:
        raise AppUsageError("--kind: give at least one of api, mcp")
    return kinds


def _store() -> app_store.AppStore:
    return app_store.default_store()


def _load(store: app_store.AppStore, login_key: str, account: str) -> AppCredentials:
    creds = store.load(login_key, account)
    if creds is None:
        raise NotFound(
            f"no app credentials for {normalize_key(login_key)}/{normalize_key(account)} in {store.where(login_key, account)} "
            "(run `plato vault app create` or `plato vault app import`)"
        )
    return creds


def _vault_rows(target: Any, login_key: str) -> list[dict]:
    rows, _ = target.run(lambda b: b.list_accounts(login_key, True))
    return rows


def _check_vault(
    login_key: str, account: str, via: str, chronos_url: str | None, api_key: str | None, console_url: str | None
) -> None:
    """The account must exist in the login vault and not be archived: an app record
    for a typo would be a grant nobody can find."""
    target = vault_main._Target(via, chronos_url, api_key, console_url)
    try:
        pick_account(_vault_rows(target, login_key), login_key, account)
    except VaultConsoleError as e:
        error = VaultConsoleError(f"{e} (pass --no-vault-check to skip this check)")
        error.exit_code = e.exit_code
        raise error from None


def _expiry(creds_or_at: datetime | None, left_s: int | None) -> str:
    if creds_or_at is None or left_s is None:
        return "-"
    if left_s <= 0:
        return f"{creds_or_at.isoformat(timespec='seconds')} (expired)"
    return f"{creds_or_at.isoformat(timespec='seconds')} (in {left_s // 3600}h {left_s % 3600 // 60}m)"


def _print_presence(creds: AppCredentials, store: app_store.AppStore, json_output: bool, **extra: Any) -> None:
    shown = creds.presence(store_path=store.where(creds.login_key, creds.account))
    if json_output:
        vault_main._print_json({**shown.model_dump(mode="json"), **extra})
        return
    console.print(
        f"[bold]{escape(shown.login_key)}/{escape(shown.account)}[/bold] "
        f"[dim]({shown.vendor}, {'+'.join(shown.kinds) or '-'})[/dim]"
    )
    _field("app", f"{shown.app_name or '-'} ({shown.app_id or 'no app id'})")
    _field("source", shown.source)
    for name in ("client_id", "client_secret", "refresh_token", "access_token"):
        _field(name, str(getattr(shown, name)))
    _field("expires_at", _expiry(shown.expires_at, shown.expires_in_s))
    _field("scopes", shown.scopes)
    _field("redirect_uri", shown.redirect_uri)
    if shown.user is not None:
        _field("user", f"{shown.user.user_id or '-'} (team {shown.user.team_id or '-'})")
    _field("store", shown.store_path)
    for key, value in extra.items():
        if value is not None:
            _field(key, value)


def _note(text: str, json_output: bool, *, raw: bool = False) -> None:
    """A progress line: stdout for people, stderr under --json so stdout stays one JSON object.
    ``raw``: plain ``print``, for a URL that a person copies. Rich wraps a long line at
    the terminal width and inserts line breaks, so a copied URL breaks."""
    if json_output:
        print(text, file=sys.stderr)
    elif raw:
        print(text, flush=True)
    else:
        console.print(text)


def _mcp_line(check: McpCheck | None) -> str | None:
    if check is None:
        return None
    if check.ok:
        return f"ok: initialize 200, tools/list 200, {check.tool_count} tools"
    tail = f", {check.error}" if check.error else ""
    hint = " (is the app's MCP switch on?)" if check.initialize_status == 200 and check.tools_status == 403 else ""
    return f"initialize {check.initialize_status}, tools/list {check.tools_status or '-'}{tail}{hint}"


def _save_locked(store: app_store.AppStore, creds: AppCredentials) -> None:
    with store.lock(creds.login_key, creds.account):
        store.save(creds)


def _finish(
    creds: AppCredentials,
    store: app_store.AppStore,
    kinds: list[CredentialKind],
    mcp: McpCheck | None,
    json_output: bool,
) -> None:
    """Print the record, then exit :data:`MCP_CHECK_EXIT_CODE` when the MCP check failed."""
    extra: dict[str, Any] = {"mcp": _mcp_line(mcp)}
    if mcp is not None:
        extra["mcp_ok"] = mcp.ok
    _print_presence(creds, store, json_output, **extra)
    if CredentialKind.mcp in kinds and mcp is not None and not mcp.ok:
        print(
            f"the MCP check failed ({_mcp_line(mcp)}). The grant is stored. Fix the app, then run "
            f"`plato vault app consent {creds.login_key} -a {creds.account} --kind mcp`",
            file=sys.stderr,
        )
        raise typer.Exit(MCP_CHECK_EXIT_CODE)


def _new_driver(
    tools: app_portal.PortalTools, browser: ConsentBrowser, login: str | None = None
) -> app_portal.BrowserDriver:
    """``login``: the account slug whose saved login the Pi browser restores and saves
    (:func:`pi_browser.login_slug`). ego-browser keeps its own profile."""
    if browser == ConsentBrowser.pi:
        return pi_browser.PiDriver(tools, login=login)
    return app_portal.EgoDriver(tools)


@contextmanager
def _driver(
    tools: app_portal.PortalTools,
    recipe: VendorRecipe,
    login_key: str,
    account: str,
    browser: ConsentBrowser = ConsentBrowser.ego,
) -> Iterator[app_portal.BrowserDriver]:
    """One TaskSpace (or Pi browser) for the command. ``finish()`` runs once at the end;
    after a hand-off it leaves the window to the person."""
    # Only this account's saved login: a shared one held another person's Canva session.
    login = pi_browser.login_slug(login_key, account) if browser == ConsentBrowser.pi else None
    driver = _new_driver(tools, browser, login)
    driver.open_space(app_portal.space_name(recipe, normalize_key(login_key), normalize_key(account)))
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


class SignIn:
    """How the consent step signs in when the vendor asks: the vault item's values (read
    only when a prompt shows) and what to do at an email code."""

    def __init__(self, secrets: Callable[[], SignInSecrets], on_email_code: OnEmailCode = OnEmailCode.person) -> None:
        self.secrets = secrets
        self.on_email_code = on_email_code

    def run(
        self, driver: app_portal.BrowserDriver, recipe: VendorRecipe, creds: AppCredentials, json_output: bool
    ) -> sign_in.SignInReport:
        return sign_in.sign_in(
            driver,
            sign_in.page_for(driver),
            recipe.sign_in,
            self.secrets,
            where=f"{creds.login_key}/{creds.account}",
            on_email_code=self.on_email_code,
            note=lambda text: _note(escape(text), json_output),
        )


def _off_consent(recipe: VendorRecipe, path: str) -> bool:
    """After a sign-in: the page is neither the consent page nor the redirect, so code
    opens the consent URL again (the vendor may land on its home page)."""
    if not path:
        return False
    redirect = urlparse(recipe.redirect_uri).path
    done = redirect.rsplit("/", 1)[0] + "/done"
    return not path.startswith(urlparse(recipe.authorize_url).path) and path not in (redirect, done)


def _drop_login(driver: app_portal.BrowserDriver) -> None:
    """The browser holds another account: the Pi stop must not save its cookies into this
    account's saved login. A window still with a person is taken back first, so the stop
    runs (finish() never stops a window after a hand-off)."""
    if driver.handed_off:
        try:
            driver.reclaim()
        except VaultConsoleError:
            pass
    driver.discard_login()


def _check_consent_account(
    driver: app_portal.BrowserDriver, recipe: VendorRecipe, creds: AppCredentials, login: SignIn | None
) -> None:
    """Before code clicks Allow on the first grant: users/me gives an id and no email, and the
    record has no earlier user to compare it with, so the consent page's account email is
    the only check. The page must not show another account email than the vault username.

    A later grant is checked by its users/me id (:func:`_check_user`). A page with no account
    email, or a vault username that is no email, gives nothing to compare: the click goes on."""
    if login is None or (creds.user is not None and creds.user.user_id):
        return
    probe = sign_in.page_for(driver).probe(recipe.sign_in)
    # check_signed_in reads only vendor_email_domains from its recipe; the sign-in recipe holds
    # the same list, so the TOTP rule (vendor and tracking addresses left out) applies here too.
    rules = recipe.sign_in
    # The first call has no username: it only filters the emails. No email means no vault read.
    if not totp_portal.check_signed_in(probe.emails, None, rules, probe.path).found:
        return
    check = totp_portal.check_signed_in(probe.emails, login.secrets().username, rules, probe.path)
    if check.result in (AccountMatch.match, AccountMatch.no_vault_email):
        return
    _drop_login(driver)
    where = f"{creds.login_key}/{creds.account}"
    others = ", ".join(e for e in check.found if e != check.expected)
    if check.result == AccountMatch.ambiguous:
        raise WrongAppAccount(
            f"the consent page shows {check.expected} and also {others}, so code cannot tell which account "
            f"grants access. Code did not click Allow, and nothing was stored"
        )
    raise WrongAppAccount(
        f"the consent page is signed in as {others}, not as {check.expected}, the username of {where}. "
        "Code did not click Allow, and nothing was stored. Sign out of that account, then run consent again"
    )


def _click_consent(
    driver: app_portal.BrowserDriver,
    recipe: VendorRecipe,
    creds: AppCredentials,
    json_output: bool,
    login: SignIn | None = None,
    url: str | None = None,
) -> None:
    """Get the grant button clicked on the consent page that ``driver`` shows.

    Code clicks first (:meth:`app_portal.EgoDriver.click_consent`): it waits for the
    button, clicks it by its accessible name, and checks that the page reached the
    redirect. The agent (or a person, when no agent binary is here) acts only when
    the code click fails.
    ``url``: the authorization URL, opened again when a code sign-in lands off the consent page."""
    _check_consent_account(driver, recipe, creds, login)
    clicked = driver.click_consent(recipe)
    if clicked.allowed:
        return
    why = f"{clicked.error or 'no reason'}, {clicked.allow_buttons or 0} button(s), {clicked.clicks or 0} click(s)"
    if driver.tools.agent is None:
        driver.hand_off()
        _note(f"The code click did not work ({why}). Click Allow in {app_portal.person_hint(driver)}.", json_output)
        return
    _note(f"The code click did not work ({why}); an agent now tries the consent page.", json_output)
    # A type-only cast, no runtime check: _driver() opened the space before this point.
    goal = app_portal.consent_goal(
        recipe, cast(int, driver.space_id), creds.app_name or creds.client_id, app_portal.driver_browser(driver)
    )
    try:
        end = driver.agent(goal, hand_off_on_need=login is None)
    except app_portal.NeedPerson as need:
        if login is None or need.reason not in sign_in.SIGN_IN_REASONS:
            raise
        # The agent stopped at a sign-in page and typed nothing: code signs in, then clicks.
        report = login.run(driver, recipe, creds, json_output)
        if not report.acted:
            # Code found no field to fill. Only an email code may go to a person
            # (--on-email-code person); a password or an authenticator code never does.
            if need.reason == "email_code" and login.on_email_code == OnEmailCode.person:
                driver.hand_off()
                raise
            if need.reason == "email_code":
                raise sign_in.EmailCodeNeeded(
                    "the consent agent stopped at an email code, and --on-email-code stop was given: nothing was "
                    f"typed{app_portal.log_hint(driver.last_agent_log)}"
                ) from None
            raise sign_in.SignInFailed(
                f"the consent agent stopped at a sign-in page ({need.reason}), but code found no sign-in field "
                f"there to fill from the vault item. Nothing was typed{app_portal.log_hint(driver.last_agent_log)}"
            ) from None
        if url is not None and _off_consent(recipe, report.path):
            # As after the first sign-in: the vendor may land on its home page, not on the consent page.
            driver.goto(url)
        # The sign-in can change the account: check the page again before this click.
        _check_consent_account(driver, recipe, creds, login)
        end = driver.click_consent(recipe)
    if not end.allowed:
        raise app_portal.PortalError(
            f"the consent agent did not allow access: {end.reason or 'no reason given'}"
            f"{app_portal.log_hint(driver.last_agent_log)}"
        )


def _note_user(user: VendorUser, json_output: bool) -> None:
    _note(f"the grant signs in as user {user.user_id or '-'} (team {user.team_id or '-'})", json_output)


def _check_user(before: AppCredentials, user: VendorUser, driver: app_portal.BrowserDriver | None) -> None:
    """users/me gives an id, no email, so code cannot compare it with the vault item; it
    compares it with the user of the record's earlier grant (check_user already rejects a reply
    with no id). Another id means the browser was signed in as another account: that grant is never stored, and the Pi keeps
    no login of that account."""
    old = before.user.user_id if before.user is not None else None
    if not old or user.user_id == old:
        return
    if driver is not None:
        _drop_login(driver)
    raise WrongAppAccount(
        f"the earlier grant of {before.login_key}/{before.account} signed in as user {old}, this one as "
        f"{user.user_id}: the browser was signed in as another account. The new grant was not "
        "stored, and the earlier one is kept. Sign in as the right account, then run consent again"
    )


def _consent(
    store: app_store.AppStore,
    recipe: VendorRecipe,
    creds: AppCredentials,
    kinds: list[CredentialKind],
    *,
    driver: app_portal.BrowserDriver | None,
    timeout_s: float,
    json_output: bool,
    login: SignIn | None = None,
) -> tuple[AppCredentials, McpCheck | None]:
    """PKCE consent, the code exchange, the user check, the store write, then the MCP check.
    ``driver`` None: the person opens the printed URL in any browser. ``login``: a sign-in
    page on the way is filled by code from the vault item (:mod:`sign_in`)."""
    pkce = app_oauth.make_pkce()
    state = app_oauth.new_state()
    url = app_oauth.authorize_url(recipe, creds.client_id, recipe.scopes_for(kinds), pkce, state)
    with app_oauth.CallbackListener(recipe.redirect_uri, state) as listener:
        if driver is None:
            _note("Open this URL in a browser signed in to the account, and allow access:", json_output)
            _note(url, json_output, raw=True)
        else:
            # Before the first page: a dead reCAPTCHA worker on a sign-in page has no detach event
            # in Playwright 1.58, so a later context.route() waits on that session and never settles.
            driver.route_callback(recipe.redirect_uri)
            driver.goto(url)
            if login is not None:
                # A browser with no session lands on the sign-in page first.
                report = login.run(driver, recipe, creds, json_output)
                if report.acted and _off_consent(recipe, report.path):
                    driver.goto(url)
            _click_consent(driver, recipe, creds, json_output, login, url)
        try:
            code = listener.wait(timeout_s, pump=driver.pump if driver is not None else None)
        except app_oauth.OAuthError as e:
            log = driver.last_agent_log if driver is not None else None
            if log is None:
                raise
            raise app_oauth.OAuthError(f"{e}{app_portal.log_hint(log)}") from None
    with app_oauth.http_client() as http:
        grant = app_oauth.exchange_code(recipe, creds.client_id, creds.client_secret, code, pkce, http)
        new = creds.with_grant(grant).model_copy(update={"kinds": kinds})
        if creds.user is not None and creds.user.user_id:
            # An earlier user to compare with: users/me runs BEFORE the save, so a grant of another
            # account never replaces the right one. A failed users/me then loses only the new grant;
            # the stored one stays, and consent can run again.
            user = app_oauth.check_user(recipe, grant.access_token, http)
            _note_user(user, json_output)
            _check_user(creds, user, driver)
            new = new.model_copy(update={"user": user})
            _save_locked(store, new)
        else:
            # The first grant: nothing to compare (the consent page check ran before the click).
            # Store before anything else can fail: the grant is new and its refresh token single-use.
            _save_locked(store, new)
            user = app_oauth.check_user(recipe, grant.access_token, http)
            _note_user(user, json_output)
            # Another process can refresh while users/me runs: re-read under the lock and
            # add only the user, so its newer refresh token is not overwritten.
            with store.lock(new.login_key, new.account):
                current = store.load(new.login_key, new.account) or new
                new = current.model_copy(update={"user": user})
                store.save(new)
        mcp = app_oauth.check_mcp(recipe, grant.access_token, http) if CredentialKind.mcp in kinds else None
    return new, mcp


@app_app.command()
def create(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. canva")],
    account: AccountArg,
    vendor: VendorArg = AppVendor.canva,
    kind: KindArg = "api,mcp",
    app_name: Annotated[
        str | None, typer.Option("--app-name", help="Name of a new app (Canva: at most 18 characters)")
    ] = None,
    app_id: Annotated[
        str | None,
        typer.Option("--app-id", help="Configure this existing app instead of creating one (keeps a stored secret)"),
    ] = None,
    manual: Annotated[
        bool, typer.Option("--manual", help="No browser agent: print the portal steps and type the values")
    ] = False,
    browser: PortalBrowserArg = ConsentBrowser.ego,
    consent: Annotated[
        bool, typer.Option("--consent/--no-consent", help="Run the consent step after the portal step")
    ] = True,
    replace: Annotated[
        bool, typer.Option("--replace", help="Replace a stored record of another app (its grant is lost)")
    ] = False,
    timeout: Annotated[int, typer.Option("--timeout", help="Seconds to wait for the consent redirect")] = 300,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print the plan; runs nothing")] = False,
    yes: YesArg = False,
    vault_check: VaultCheckArg = True,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Create (or, with --app-id, configure) the vendor app in its developer portal, store
    its client id and secret, then run the consent. An agent in ego-browser (or, with
    --browser pi, on the Pi screen) does the clicks; code clicks "Generate secret" and
    reads it, so no model sees it. Runs a paid agent and changes the live vendor
    account, so --yes is required."""
    with vault_main._errors(json_output):
        if browser == ConsentBrowser.none:
            raise AppUsageError("--browser none: `create` needs a browser; pass --manual to do the portal by hand")
        recipe = RECIPES[vendor]
        kinds = _parse_kinds(kind, [CredentialKind.api])
        name = app_name or (None if app_id else f"plato-{normalize_key(account)}"[: recipe.app_name_max])
        if name and len(name) > recipe.app_name_max:
            raise AppUsageError(f"--app-name: at most {recipe.app_name_max} characters for {vendor}")
        store = _store()
        existing = store.load(login_key, account)
        if existing is not None and not replace and (app_id is None or existing.app_id != app_id):
            raise AppUsageError(
                f"{normalize_key(login_key)}/{normalize_key(account)} already has app "
                f"{existing.app_name or '-'} ({existing.app_id or 'no app id'}). Pass --app-id "
                f"{existing.app_id or '<id>'} to change its settings, or --replace to store a new app"
            )
        keep_secret = existing is not None and app_id is not None and existing.app_id == app_id
        plan = {
            "vendor": vendor.value,
            "portal": recipe.portal_url,
            "app": f"existing {app_id}" if app_id else f"new app {name!r}",
            "kinds": [k.value for k in kinds],
            "switches": [recipe.switches[k] for k in kinds],
            "scopes": recipe.scopes_for(kinds),
            "redirect_uri": recipe.redirect_uri,
            "secret": "keep the stored secret" if keep_secret else "generate a new secret",
            "consent": consent,
            "browser": "manual" if manual else _BROWSER_PLAN[browser],
            "store": store.where(login_key, account),
        }
        if dry_run:
            if json_output:
                vault_main._print_json({"dry_run": True, "plan": plan})
            else:
                console.print("[yellow]dry run - nothing ran[/yellow]")
                for key, value in plan.items():
                    _field(key, value)
            return
        if not manual and not yes:
            raise VaultConsoleError(
                "refusing to run: `create` runs a paid browser agent and changes the live vendor account. "
                "Re-run with --yes, or --dry-run to see the plan."
            )
        if vault_check:
            _check_vault(login_key, account, via, chronos_url, api_key, console_url)

        now = datetime.now(UTC)

        def record(
            client_id: str, secret: SecretStr, source: CredentialSource, got_app_id: str | None
        ) -> AppCredentials:
            return AppCredentials(
                vendor=vendor,
                login_key=normalize_key(login_key),
                account=normalize_key(account),
                kinds=kinds,
                app_id=got_app_id,
                app_name=name,
                client_id=client_id,
                client_secret=secret,
                client_auth=recipe.client_auth,
                source=source,
                redirect_uri=recipe.redirect_uri,
                created_at=now,
                updated_at=now,
            )

        if manual:
            creds = existing if keep_secret else None
            if creds is None:
                _manual_steps(recipe, kinds, name, app_id, json_output)
                # err=: under --json, prompts go to stderr so stdout stays one JSON object.
                client_id = typer.prompt("client id", err=json_output).strip()
                secret = getpass.getpass("client secret (not shown): ").strip()
                if not client_id.startswith(recipe.client_id_prefix) or not secret:
                    raise AppUsageError(
                        f"the client id must start {recipe.client_id_prefix} and the secret is required"
                    )
                got_app = (
                    app_id or typer.prompt("app id (from the portal URL)", default="", err=json_output).strip()
                ) or None
                creds = record(client_id, SecretStr(secret), CredentialSource.typed, got_app)
                _save_locked(store, creds)
            mcp = None
            if consent:
                creds, mcp = _consent(
                    store, recipe, creds, kinds, driver=None, timeout_s=timeout, json_output=json_output
                )
            _finish(creds, store, kinds, mcp, json_output)
            return

        tools = app_portal.find_tools()
        if tools.agent is None:
            raise app_portal.PortalUnavailable("no `claude` binary here for the portal agent: pass --manual")
        with _driver(tools, recipe, login_key, account, browser) as driver:
            driver.goto(recipe.portal_url)
            result = app_portal.run_portal(
                driver, recipe, kinds, app_name=name, app_id=app_id, generate_secret=not keep_secret
            )
            if keep_secret:
                assert existing is not None
                creds = existing
            else:
                assert result.client_id is not None and result.client_secret is not None
                creds = record(result.client_id, result.client_secret, CredentialSource.portal, result.app_id)
                _save_locked(store, creds)
                _note(
                    f"stored the new secret ({creds.client_secret.get_secret_value()[:3]}..., "
                    f"{len(creds.client_secret.get_secret_value())} chars)",
                    json_output,
                )
            mcp = None
            if consent:
                login = SignIn(sign_in.vault_secrets(login_key, account, chronos_url, api_key))
                creds, mcp = _consent(
                    store, recipe, creds, kinds, driver=driver, timeout_s=timeout, json_output=json_output, login=login
                )
        if result.notice:
            _note("ego-browser says an update is available: run `ego-browser upgrade` when it suits you", json_output)
        _finish(creds, store, kinds, mcp, json_output)


def _manual_steps(
    recipe: VendorRecipe, kinds: list[CredentialKind], name: str | None, app_id: str | None, json_output: bool
) -> None:
    """The portal steps for a person, through :func:`_note` (stderr under --json)."""
    _note(f"1. Open {recipe.portal_url}.", json_output)
    if app_id:
        _note(f"2. Open the app {escape(app_id)}.", json_output)
    else:
        _note(
            f"2. Create an app named {escape(name or '')!r}: Public, tick the Developer Terms, Outside Canva.",
            json_output,
        )
    _note(f"3. Turn on: {', '.join(recipe.switches[k] for k in kinds)}.", json_output)
    _note(f"4. Tick these scopes: {' '.join(recipe.scopes_for(kinds))}.", json_output)
    _note(f"5. Add the redirect URL {recipe.redirect_uri}.", json_output)
    _note("6. Click Generate secret, then type the client id and the secret below.", json_output)


@app_app.command("import")
def import_env(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. canva")],
    account: AccountArg,
    env_file: Annotated[
        Path, typer.Option("--env-file", help="The env file to adopt, e.g. ~/.plato-creds/canva-connect.env")
    ],
    vendor: VendorArg = AppVendor.canva,
    kind: KindArg = "api",
    app_id: Annotated[str | None, typer.Option("--app-id", help="The app's id in the vendor portal")] = None,
    app_name: Annotated[str | None, typer.Option("--app-name", help="The app's name in the vendor portal")] = None,
    replace: Annotated[
        bool, typer.Option("--replace", help="Replace a stored record (a newer refresh token in it is lost)")
    ] = False,
    vault_check: VaultCheckArg = True,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Adopt an existing app's credentials from an env file: <V>_CLIENT_ID, _CLIENT_SECRET,
    _REFRESH_TOKEN, _ACCESS_TOKEN (also with _API_ or _MCP_ after the vendor name). The file
    is only read. After the next refresh its refresh token is spent: do not use it elsewhere."""
    with vault_main._errors(json_output):
        recipe = RECIPES[vendor]
        kinds = _parse_kinds(kind, [CredentialKind.api])
        store = _store()
        if not replace:
            _refuse_existing(store, login_key, account)
        if vault_check:
            _check_vault(login_key, account, via, chronos_url, api_key, console_url)
        values, mapping = map_env(read_env_file(env_file), vendor)
        if "client_id" not in values or "client_secret" not in values:
            raise AppUsageError(
                f"{env_file} has no client id or no client secret for {vendor} (names: {_names_hint(vendor)})"
            )
        now = datetime.now(UTC)
        access = values.get("access_token")
        creds = AppCredentials(
            vendor=vendor,
            login_key=normalize_key(login_key),
            account=normalize_key(account),
            kinds=kinds,
            app_id=app_id,
            app_name=app_name,
            client_id=values["client_id"],
            client_secret=SecretStr(values["client_secret"]),
            client_auth=recipe.client_auth,
            source=CredentialSource.imported,
            redirect_uri=recipe.redirect_uri,
            scopes=recipe.scopes_for(kinds),
            refresh_token=SecretStr(values["refresh_token"]) if values.get("refresh_token") else None,
            access_token=SecretStr(access) if access else None,
            expires_at=jwt_expiry(access) if access else None,
            created_at=now,
            updated_at=now,
        )
        # Again under the lock: another import may have saved since the check above.
        with store.lock(creds.login_key, creds.account):
            if not replace:
                _refuse_existing(store, login_key, account)
            store.save(creds)
    if not json_output:
        for env_name, field in mapping.items():
            console.print(f"  {escape(env_name)} -> {field}")
        console.print(
            f"[yellow]{escape(str(env_file))} still holds the refresh token. After the next refresh it is spent: "
            "do not use that file for refreshes any more.[/yellow]"
        )
    _print_presence(creds, store, json_output, mapped=mapping if json_output else None)


def _refuse_existing(store: app_store.AppStore, login_key: str, account: str) -> None:
    if store.load(login_key, account) is not None:
        raise AppUsageError(
            f"{normalize_key(login_key)}/{normalize_key(account)} already has a stored record; "
            "pass --replace to overwrite it (its refresh token may be newer than the file's)"
        )


_ENV_FIELDS = {
    "CLIENT_ID": "client_id",
    "CLIENT_SECRET": "client_secret",
    "REFRESH_TOKEN": "refresh_token",
    "ACCESS_TOKEN": "access_token",
}


def _names_hint(vendor: AppVendor) -> str:
    v = vendor.value.upper()
    return ", ".join(f"{v}_{suffix}" for suffix in _ENV_FIELDS)


def read_env_file(path: Path) -> dict[str, str]:
    """``NAME=value`` lines; ``export``, comments, blank lines and one level of quotes are handled."""
    try:
        text = path.expanduser().read_text()
    except OSError as e:
        raise AppUsageError(f"cannot read {path}: {e.strerror}") from None
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        name, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[name.strip()] = value
    return out


def map_env(env: dict[str, str], vendor: AppVendor) -> tuple[dict[str, str], dict[str, str]]:
    """``(values by field, env name -> field)``. ``CANVA_CLIENT_ID``, ``CANVA_API_CLIENT_ID``
    and ``CANVA_MCP_CLIENT_ID`` all map to ``client_id``; two names with different
    values for one field are refused (which one is current?)."""
    v = vendor.value.upper()
    values: dict[str, str] = {}
    mapping: dict[str, str] = {}
    for suffix, field in _ENV_FIELDS.items():
        for name in (f"{v}_{suffix}", f"{v}_API_{suffix}", f"{v}_MCP_{suffix}"):
            value = env.get(name)
            if not value:
                continue
            if field in values and values[field] != value:
                raise AppUsageError(
                    f"two names hold different values for {field} ({', '.join(sorted(mapping))}, {name})"
                )
            values[field] = value
            mapping[name] = field
    return values, mapping


def jwt_expiry(token: str) -> datetime | None:
    """The ``exp`` claim of a JWT access token, unverified; None when it is not a JWT."""
    parts = token.split(".")
    if len(parts) != 3:
        return None
    try:
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4)))
        exp = payload.get("exp") if isinstance(payload, dict) else None
        return datetime.fromtimestamp(int(exp), UTC) if exp is not None else None
    except (ValueError, TypeError, OverflowError):
        return None


@app_app.command("consent")
def consent_cmd(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. canva")],
    account: AccountArg,
    kind: KindArg = None,
    browser: Annotated[
        ConsentBrowser,
        typer.Option(
            "--browser",
            help="pi (the default): Chromium on pi5-2 (noVNC for a person); ego: ego-browser on this Mac; "
            "none: print the URL. With pi and ego, code signs in from the vault item and clicks Allow",
        ),
    ] = ConsentBrowser.pi,
    on_email_code: sign_in.OnEmailCodeArg = OnEmailCode.person,
    timeout: Annotated[int, typer.Option("--timeout", help="Seconds to wait for the consent redirect")] = 300,
    yes: YesArg = False,
    vault_check: VaultCheckArg = True,
    via: ViaArg = "chronos",
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Get a new grant (PKCE consent and code exchange) for the stored app, store it, and
    check it (users/me; MCP initialize and tools/list for --kind mcp). The new grant
    replaces the stored one. --kind defaults to the stored kinds. A sign-in page on the
    way is filled by code from the vault item (needs PLATO_API_KEY); only a code that the
    vendor sends by email needs a person (--on-email-code)."""
    with vault_main._errors(json_output):
        store = _store()
        creds = _load(store, login_key, account)
        recipe = RECIPES[creds.vendor]
        kinds = _parse_kinds(kind, creds.kinds)
        if browser != ConsentBrowser.none and not yes:
            raise VaultConsoleError(
                f"refusing to run: `--browser {browser.value}` can run a paid agent that clicks Allow. "
                "Re-run with --yes, or use --browser none and open the URL yourself."
            )
        if vault_check:
            _check_vault(login_key, account, via, chronos_url, api_key, console_url)
        if browser == ConsentBrowser.none:
            creds, mcp = _consent(store, recipe, creds, kinds, driver=None, timeout_s=timeout, json_output=json_output)
        else:
            tools = app_portal.find_tools()
            if browser == ConsentBrowser.ego and tools.ego is None:
                raise app_portal.PortalUnavailable(
                    "ego-browser is not installed here: use --browser pi, or --browser none and open the printed "
                    "URL yourself"
                )
            login = SignIn(sign_in.vault_secrets(login_key, account, chronos_url, api_key), on_email_code)
            with _driver(tools, recipe, login_key, account, browser) as driver:
                creds, mcp = _consent(
                    store, recipe, creds, kinds, driver=driver, timeout_s=timeout, json_output=json_output, login=login
                )
        _finish(creds, store, kinds, mcp, json_output)


@app_app.command("refresh")
def refresh_cmd(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. canva")],
    account: AccountArg,
    json_output: JsonArg = False,
):
    """Rotate the grant now: one refresh under the account lock, stored before anything uses it."""
    with vault_main._errors(json_output):
        store = _store()
        recipe = RECIPES[_load(store, login_key, account).vendor]
        with app_oauth.http_client() as http:
            creds, _ = app_oauth.refresh(store, recipe, login_key, account, http)
        _print_presence(creds, store, json_output, refreshed=True)


@app_app.command("show")
def show_cmd(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. canva")],
    account: AccountArg,
    json_output: JsonArg = False,
):
    """The stored record: presence, first characters and length of each value, and the expiry. No secret."""
    with vault_main._errors(json_output):
        store = _store()
        creds = _load(store, login_key, account)
        _print_presence(creds, store, json_output)


def token_env(creds: AppCredentials, recipe: VendorRecipe, kinds: list[CredentialKind]) -> dict[str, str]:
    """The env names `token` writes. An access token, never the refresh token or the client secret."""
    assert creds.access_token is not None
    out: dict[str, str] = {}
    for kind in kinds:
        prefix = recipe.env_prefix[kind]
        out[f"{prefix}_ACCESS_TOKEN"] = creds.access_token.get_secret_value()
        out[f"{prefix}_CLIENT_ID"] = creds.client_id
        if creds.expires_at is not None:
            out[f"{prefix}_EXPIRES_AT"] = creds.expires_at.isoformat(timespec="seconds")
        if kind == CredentialKind.mcp:
            out[f"{prefix}_URL"] = recipe.mcp_url
    return out


@app_app.command("token")
def token_cmd(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. canva")],
    account: AccountArg,
    env_file: Annotated[Path, typer.Option("--env-file", help="Where to write the access token (mode 600)")],
    kind: KindArg = None,
    min_left: Annotated[
        int, typer.Option("--min-left", help="Refresh first when the access token has fewer seconds left")
    ] = TOKEN_MIN_LEFT_S,
    json_output: JsonArg = False,
):
    """Write a fresh access token to an env file for a local run (CANVA_API_* and CANVA_MCP_*).
    Refreshes first when less than --min-left seconds are left. Never writes the refresh token."""
    with vault_main._errors(json_output):
        store = _store()
        stored = _load(store, login_key, account)
        recipe = RECIPES[stored.vendor]
        kinds = _parse_kinds(kind, stored.kinds)
        missing = [k for k in kinds if k not in stored.kinds]
        if missing:
            raise AppUsageError(
                f"the stored grant does not serve {', '.join(missing)} (it serves {', '.join(stored.kinds)}); "
                f"run `plato vault app consent {login_key} -a {account} --kind {','.join(kinds)}`"
            )
        with app_oauth.http_client() as http:
            creds, refreshed = app_oauth.refresh(store, recipe, login_key, account, http, min_left_s=min_left)
        values = token_env(creds, recipe, kinds)
        path = env_file.expanduser()
        stamp = datetime.now(UTC).isoformat(timespec="seconds")
        body = f"# plato vault app token {creds.login_key}/{creds.account} at {stamp}; no refresh token here\n"
        body += "".join(f"{name}={value}\n" for name, value in values.items())
        app_store.atomic_write(path, body)
        report = TokenFileReport(path=str(path), names=list(values), refreshed=refreshed, expires_at=creds.expires_at)
    if json_output:
        vault_main._print_json(report.model_dump(mode="json"))
        return
    console.print(
        f"[green]wrote[/green] {escape(report.path)} [dim](mode 600{', refreshed' if refreshed else ''})[/dim]"
    )
    _field("names", report.names)
    left = creds.seconds_left()
    _field("expires_at", _expiry(creds.expires_at, int(left) if left is not None else None))
