"""`plato vault signup`: make a vault account for a persona (``not_started``) and
launch the login world in sign-up mode, so an agent signs it up on the site.

:func:`prepare_signup_account` makes the account (username = the persona's email,
a generated password, ``account_status: not_started``) and links the persona: the
step an orchestrator may do on its own. :func:`launch_signup` launches the vault
org's login-agent template (what `plato vault open` and a bake launch) with
``mode: signup`` and the account on top. The world checks the rest
(login_world/signup.py): the app allows sign-ups, the account is ``not_started``;
it ends ``done``, or ``not_started`` again.
"""

from __future__ import annotations

import os
import secrets
import string
from typing import Annotated, Any

import typer
from pydantic import BaseModel
from rich.markup import escape

from plato.chronos.login_vault import AccountStatus, LoginVault, normalize_key
from plato.cli.chronos.settings import get_settings
from plato.cli.utils import console
from plato.cli.vault.backends import chronos_errors
from plato.cli.vault.client import VaultConsoleError
from plato.cli.vault.open_session import (
    BROWSERBASE_KEYS,
    OP_TOKEN,
    OP_VAULT,
    LoginSettings,
    OpenClient,
    _ltree_tag,
)

# The config field only a login world with this sign-up mode has: an older world
# ignores unknown fields and would run an ordinary bake of an account that
# does not exist on the site.
SIGNUP_MODE_FIELD = "enroll_totp"
PASSWORD_LENGTH = 20
_PASSWORD_SYMBOLS = "!@#%^*-_=+"
SIGNUP_TAG = "vault_signup"


class SignupLaunch(BaseModel):
    """What :func:`launch_signup` started (``session_id`` is None on a dry run)."""

    session_id: str | None
    session_url: str | None
    launch: dict[str, Any]


def generate_password(length: int = PASSWORD_LENGTH) -> str:
    """A password that meets the usual rules: lower, upper, digit and symbol."""
    pools = (string.ascii_lowercase, string.ascii_uppercase, string.digits, _PASSWORD_SYMBOLS)
    chars = [secrets.choice(pool) for pool in pools]
    chars += [secrets.choice("".join(pools)) for _ in range(length - len(pools))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def prepare_signup_account(
    vault: LoginVault, login_key: str, account: str, persona: str, signup_url: str | None = None
) -> str:
    """Make ``login_key/account`` for ``persona`` (its email as the username, a
    generated password, ``not_started``, the app's login page as its ``login_url``,
    else ``signup_url``, so `plato vault open` can open it once it exists) and link
    the persona. An account that exists is left as it is (the world checks its
    status). Answers what it did."""
    lk, ac, who = normalize_key(login_key), normalize_key(account), normalize_key(persona)
    found = next((p for p in vault.list_personas().personas if p.persona == who), None)
    if found is None:
        raise VaultConsoleError(f"no persona {who}: make it with `plato vault personas set {who} --email ...`")
    existing = next((a for a in vault.list_accounts(lk, True).accounts if a.account == ac), None)
    if existing is not None:
        # Only an unfinished sign-up of this persona (not_started, its email as the
        # username) whose link failed is finished here, its password kept; any
        # other account is left as it is (the world refuses it).
        unfinished = getattr(existing, "account_status", None) == AccountStatus.NOT_STARTED and (
            (existing.username or "").casefold() == found.email.casefold()
        )
        if unfinished and vault.get_account_persona(lk, ac) is None:
            vault.set_account_persona(lk, ac, {"person_key": who})
            return "linked"
        return "exists"
    fields: dict[str, str] = {}
    if login_url := app_login_url(vault, lk) or signup_url:
        fields["login_url"] = login_url
    vault.create_account(
        lk,
        ac,
        username=found.email,
        password=generate_password(),
        account_status=AccountStatus.NOT_STARTED.value,
        **fields,
    )
    vault.set_account_persona(lk, ac, {"person_key": who})
    return "created"


def check_signup_world(schema: Any, world_package: str) -> None:
    """Refuse a login world without sign-up mode."""
    config_schema = getattr(schema, "config_schema", None)
    if hasattr(config_schema, "model_dump"):
        config_schema = config_schema.model_dump()
    properties = config_schema.get("properties") if isinstance(config_schema, dict) else None
    if SIGNUP_MODE_FIELD not in (properties or {}):
        version = getattr(schema, "version", None) or "?"
        raise VaultConsoleError(
            f"{world_package} (version {version}) has no sign-up mode yet. Wait for the login "
            "world release, or pass --world-package with a version that has it"
        )


def build_signup_launch(
    *,
    login_key: str,
    account: str,
    signup_url: str,
    settings: LoginSettings,
    signup_hint: str | None = None,
    enroll_totp: bool = True,
    proxy_exit: str | None = None,
    world_package: str | None = None,
) -> dict[str, Any]:
    """The ``/api/jobs/launch`` body: the login-agent template filled for this
    account, sign-up keys on top. Secret-free: every key is a ``${...}`` that
    Chronos fills. A sign-up runs on the agent VM's Chrome, so the template's
    Browserbase keys are dropped."""
    lk, ac = normalize_key(login_key), normalize_key(account)
    if not (lk and ac and signup_url.strip()):
        raise VaultConsoleError("sign-up needs the app, --account and --url")
    settings = settings.filled(LOGIN_KEY=lk, LOGIN_ACCOUNT=ac, LOGIN_URL=signup_url, LOGIN_VAULT=OP_VAULT)
    agent = settings.world.config.agent
    config: dict[str, Any] = {
        **{k: v for k, v in settings.world.config.model_dump(mode="json").items() if k not in BROWSERBASE_KEYS},
        "mode": "signup",
        "clone_name": lk,
        "login_key": lk,
        "account": ac,
        "target_url": signup_url,
        "signup_url": signup_url,
        "enroll_totp": enroll_totp,
        "op_service_account_token": OP_TOKEN,
        "op_vault": OP_VAULT,
        "cdp_browser": False,
        "agent_types_password": False,
        "agent": {
            "package": agent.package,
            **({"agent_name": agent.agent_name} if agent.agent_name else {}),
            "config": dict(agent.config),
        },
    }
    if signup_hint:
        config["signup_hint"] = signup_hint
    if proxy_exit:
        config["proxy_exit"] = proxy_exit
    tags = [lk, ac, SIGNUP_TAG, f"login_key:{lk}", f"account:{ac}"]
    tags.append(f"login_agent:v{settings.version}")
    return {
        "tags": [_ltree_tag(t) for t in tags],
        "world": {
            "package": world_package or settings.world.package,
            "runtime": {"type": "vm", "vm": settings.world.runtime.vm.model_dump(exclude_none=True)},
            "config": config,
        },
    }


def app_login_url(vault: LoginVault, login_key: str) -> str | None:
    """The app's login page: its default account's ``login_url`` (else any of its
    accounts'). A sign-up with no URL starts there and finds the sign-up link."""
    lk = normalize_key(login_key)
    accounts = vault.list_accounts(lk).accounts
    ordered = sorted(accounts, key=lambda a: lk not in (getattr(a, "default_for", None) or []))
    return next((a.login_url for a in ordered if getattr(a, "login_url", None)), None)


def launch_signup(
    login_key: str,
    account: str,
    signup_url: str | None = None,
    *,
    persona: str | None = None,
    signup_hint: str | None = None,
    enroll_totp: bool = True,
    proxy_exit: str | None = None,
    world_package: str | None = None,
    api_key: str | None = None,
    chronos_url: str | None = None,
    dry_run: bool = False,
) -> SignupLaunch:
    """Launch one sign-up run with the caller's Plato key (``PLATO_API_KEY``).
    With ``persona``, first make the account for it when it does not exist
    (:func:`prepare_signup_account`; not on a dry run). ``signup_url`` is saved
    as the app's sign-up page when it has none; without one, the app's saved
    page, else its login page (:func:`app_login_url`). Raises
    :class:`VaultConsoleError` for a refusal it can see before the launch."""
    key = api_key or os.environ.get("PLATO_API_KEY") or ""
    if not key:
        raise VaultConsoleError("sign-up launches through Chronos with your Plato key: set PLATO_API_KEY")
    base = (chronos_url or get_settings().chronos_url).rstrip("/")
    with LoginVault(api_key=key, base_url=base) as vault, chronos_errors(base):
        app = vault.get_app_settings(normalize_key(login_key))
        if not app.signup_allowed:
            # The world refuses it too; refusing here writes no account and launches nothing.
            raise VaultConsoleError(
                f"sign-up is off for {normalize_key(login_key)}: a person turns it on "
                f"(`plato vault edit {normalize_key(login_key)} --signup-allowed`) once the site's terms allow it"
            )
        saved = app.signup_url
        if signup_url and not saved and not dry_run:
            # The app's sign-up page, set once: later sign-ups need no --url.
            vault.update_app_settings(normalize_key(login_key), signup_url=signup_url)
        signup_url = signup_url or saved or app_login_url(vault, login_key)
        if not signup_url:
            raise VaultConsoleError(f"{login_key} has no sign-up or login page in the vault: pass --url")
        if persona and not dry_run:
            prepare_signup_account(vault, login_key, account, persona, signup_url)
    client = OpenClient(base, key)
    try:
        with chronos_errors(base):
            settings = client.login_settings()
            package = world_package or settings.world.package
            check_signup_world(client.world_schema(package), package)
            body = build_signup_launch(
                login_key=login_key,
                account=account,
                signup_url=signup_url,
                settings=settings,
                signup_hint=signup_hint,
                enroll_totp=enroll_totp,
                proxy_exit=proxy_exit,
                world_package=package,
            )
            if dry_run:
                return SignupLaunch(session_id=None, session_url=None, launch=body)
            session_id = client.launch(body)
    finally:
        client.close()
    return SignupLaunch(
        session_id=session_id or None,
        session_url=f"{base}/sessions/{session_id}" if session_id else None,
        launch=body,
    )


def signup(
    login_key: Annotated[str, typer.Argument(help="Which app, e.g. todoist (its login_key)")],
    account: Annotated[str, typer.Option("--account", "-a", help="The new account's name in the vault")],
    url: Annotated[
        str | None,
        typer.Option(
            "--url",
            help="The site's sign-up page, saved for the app the first time (else the app's saved one, "
            "else its login page)",
        ),
    ] = None,
    persona: Annotated[
        str | None,
        typer.Option(
            "--persona",
            help="Make the account for this persona first (`plato vault free --login-key <app>`); "
            "omit when the account exists (not_started)",
        ),
    ] = None,
    hint: Annotated[
        str | None, typer.Option("--hint", help="Sign-up steps for the agent (else the app's signup_hint)")
    ] = None,
    totp: Annotated[
        bool, typer.Option("--totp/--no-totp", help="Turn on authenticator 2FA when the site offers it")
    ] = True,
    proxy_exit: Annotated[str | None, typer.Option("--exit", help="Proxy exit name (else the app's)")] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print the launch; launches nothing")] = False,
    world_package: Annotated[
        str | None, typer.Option("--world-package", hidden=True, help="Login world to launch (a dev build, say)")
    ] = None,
    chronos_url: Annotated[str | None, typer.Option("--chronos-url", hidden=True)] = None,
    api_key: Annotated[str | None, typer.Option("--api-key", hidden=True)] = None,
    json_output: Annotated[bool, typer.Option("--json", help="Print JSON")] = False,
):
    """Sign an account up on its site (a login-world run in sign-up mode).

    With --persona and no such account yet, it first makes the vault account
    (the persona's email, a generated password, account_status not_started) and
    links the persona. The run signs up only where the app allows it
    (`signup_allowed`, a person turns it on) and only a not_started account; the
    account ends done, or not_started again. A CAPTCHA gets at most 3
    tries, then the run ends login_blocked for a person; a site that refuses
    outright is never worked around. Costs money: it runs a VM and an agent.
    """
    from plato.cli.vault.main import _fail, _print_json

    try:
        result = launch_signup(
            login_key,
            account,
            url,
            persona=persona,
            signup_hint=hint,
            enroll_totp=totp,
            proxy_exit=proxy_exit,
            world_package=world_package,
            api_key=api_key,
            chronos_url=chronos_url,
            dry_run=dry_run,
        )
    except VaultConsoleError as e:
        _fail(e, json_output)
    if json_output:
        _print_json(result.model_dump(mode="json"))
        return
    if dry_run:
        console.print("[yellow]dry run - nothing launched[/yellow]")
        _print_json(result.launch)
        return
    lk, ac = normalize_key(login_key), normalize_key(account)
    console.print(f"[green]signing up[/green] {escape(lk)}/{escape(ac)}")
    console.print(f"  session: {escape(result.session_url or 'unknown')}")
