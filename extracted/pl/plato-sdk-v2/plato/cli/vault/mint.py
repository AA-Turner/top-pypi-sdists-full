"""`plato vault mint token`: make sure a vault account has a working OAuth grant in the login
vault, for any vendor. Verifies the stored grant first; only a missing or dead one runs the
agent (:mod:`app_mint`). Prints names, lengths and HTTP statuses, never a value."""

from __future__ import annotations

import os
import re
from typing import Annotated

import typer

from plato.cli.utils import console
from plato.cli.vault import app_mint, app_portal
from plato.cli.vault import main as vault_main
from plato.cli.vault.app import _check_vault
from plato.cli.vault.client import VaultConsoleError
from plato.cli.vault.main import AccountArg, ApiKeyArg, ChronosUrlArg, JsonArg, _field
from plato.cli.vault.mint_models import GRANT_KIND_PATTERN, MintOutcome, MintReport
from plato.cli.vault.mint_store import GrantStore


class MintUsageError(VaultConsoleError):
    """A bad option, or a mint without --yes. Nothing was sent. Exit 2."""

    exit_code = 2


mint_app = typer.Typer(
    help="Make sure a vault account has a working API credential in the login vault, for any vendor.",
    # Frame locals hold the vault item and tokens: never print them in a traceback.
    pretty_exceptions_show_locals=False,
)


@mint_app.command("token")
def token_cmd(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. jira or figma")],
    account: AccountArg,
    kind: Annotated[
        str, typer.Option("--kind", help="The grant kind in the login vault (api: the vendor's REST API)")
    ] = "api",
    replace: Annotated[
        bool, typer.Option("--replace", help="Mint a new grant even when the stored one works, and replace it")
    ] = False,
    check_url: Annotated[
        str | None,
        typer.Option(
            "--check-url",
            help="Also verify a stored grant with this GET endpoint of the vendor (e.g. a 'who am I' URL)",
        ),
    ] = None,
    vendor_domain: Annotated[
        list[str] | None,
        typer.Option(
            "--vendor-domain",
            help="Another domain of the vendor (with its subdomains) besides the vault login URL's host "
            "(e.g. googleapis.com); repeatable",
        ),
    ] = None,
    hint: Annotated[
        str | None,
        typer.Option("--hint", help="A note for the agent, e.g. 'install the app on plato-plans.atlassian.net'"),
    ] = None,
    model: Annotated[str | None, typer.Option("--model", help="The agent's model (claude --model)")] = None,
    timeout: Annotated[int, typer.Option("--timeout", help="Seconds the agent may run")] = int(app_mint.MINT_TIMEOUT_S),
    yes: Annotated[
        bool, typer.Option("--yes", help="Required to mint: the agent costs money and changes the vendor account")
    ] = False,
    chronos_url: ChronosUrlArg = None,
    api_key: ApiKeyArg = None,
    json_output: JsonArg = False,
):
    """Verify the account's grant (present, active, its token read through Chronos answers; with
    --check-url also that vendor call). When it is missing or dead, a computer-use agent on the
    office Pi browser finds the vendor's developer docs, makes (or reuses) the OAuth app
    'plato-vault-mint' and runs the consent; code signs in from the vault item, reads the client
    secret, exchanges the code and moves the grant into the login vault, where Chronos refreshes it
    on demand. Grant writes need a person's own PLATO_API_KEY."""
    with vault_main._errors(json_output):
        if not re.fullmatch(GRANT_KIND_PATTERN, kind):
            raise MintUsageError(f"--kind must match {GRANT_KIND_PATTERN}")
        key = api_key or os.environ.get("PLATO_API_KEY") or ""
        if not key:
            raise MintUsageError("set PLATO_API_KEY or pass --api-key (the login vault needs it)")
        run = app_mint.MintRun(
            login_key=login_key,
            account=account,
            kind=kind,
            hint=hint,
            vendor_domains=vendor_domain or [],
            check_url=check_url,
            replace=replace,
            model=model,
            timeout_s=float(timeout),
        )
        _check_vault(login_key, account, "chronos", chronos_url, key, None)
        item = app_mint.read_vault_item(login_key, account, chronos_url, key)
        with GrantStore(app_mint.chronos_url_of(chronos_url), key) as store:
            if not yes and not replace:
                report = app_mint.verify_only(run, item, store)
                if report.outcome != MintOutcome.verified:
                    raise MintUsageError(
                        f"{report.login_key}/{report.account} needs a new {kind} grant ({report.why_mint}). Minting "
                        "runs a paid agent that changes the vendor account: re-run with --yes"
                    )
            else:
                if not yes:
                    raise MintUsageError("--replace mints a new grant with a paid agent: add --yes")
                report = app_mint.run_mint(run, item, store, app_portal.find_tools())
        _print(report, json_output)


def _print(report: MintReport, json_output: bool) -> None:
    if json_output:
        vault_main._print_json(report.model_dump(mode="json", exclude_none=True))
        return
    console.print(f"[bold]{report.login_key}/{report.account}[/bold] [dim]({report.kind} grant)[/dim]")
    _field("outcome", str(report.outcome))
    if report.why_mint:
        _field("why minted", report.why_mint)
    if report.summary:
        _field("agent", report.summary)
    if report.values:
        _field("read values", ", ".join(f"{k} ({v} chars)" for k, v in report.values.items()))
    _field("state", f"{report.state or '-'}, generation {report.generation}, {report.scopes or 0} scopes")
    _field("token read", f"refreshed={report.refreshed}, expires {report.expires_at or '-'}")
    if report.check_url:
        checked = report.stored_check
        _field("check", f"{report.check_url}: HTTP {checked.status if checked else '-'}")
