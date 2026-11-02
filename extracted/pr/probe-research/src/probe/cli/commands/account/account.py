"""probe login / logout / whoami: sign this machine in or out, holding the daemon's key while who is signed in changes."""

from __future__ import annotations
import sys

import typer

from .... import errors
from ....sdk.settings.settings import (
    DEFAULT_BASE_URL,
    clear_context,
    current_context_name,
    load_context,
    resolve,
    save_context,
    use_context)
from ....sdk.settings.device import (
    DeviceLoginError,
    OnboardingRequired,
    device_login)
from probe.cli.cli import app


@app.command()
def login(
    base_url: str = typer.Option(None, "--base-url"),
    token: str = typer.Option(None, "--token"),
    ingest_token: str = typer.Option(None, "--ingest-token"),
    hmac_secret: str = typer.Option(None, "--hmac-secret"),
    device: bool = typer.Option(
        True,
        "--device/--endpoint-only",
        help="browser-assisted login (the default); --endpoint-only saves the endpoint without minting a token",
    ),
    context: str = typer.Option(
        None, "--context", help="name the context to create or overwrite (default: the active one)"
    ),
) -> None:
    """Log in. Bare ``probe login`` runs the browser handoff (RFC 8628) — approve
    in the dashboard, no token to see or paste.

    Pass ``--token probe_pat_...`` for the air-gap paste path, or
    ``--endpoint-only`` to just save ``--base-url`` without minting a token.

    ``--context staging`` logs in under a named context instead of the active one,
    so several endpoints or tenants can coexist on one machine.
    """
    from probe.cli.wizard.session.run_lock import _wizard_run_lock
    with _wizard_run_lock(command="probe login"):
        _login(
            base_url=base_url,
            token=token,
            ingest_token=ingest_token,
            hmac_secret=hmac_secret,
            device=device,
            context=context,
        )


def _login(
    *,
    base_url: str | None,
    token: str | None,
    ingest_token: str | None,
    hmac_secret: str | None,
    device: bool,
    context: str | None,
    open_browser: bool = True,
) -> None:
    """Sign this machine in, and ONLY that: no plugin, capture or rule is touched.

    `probe wizard --action login` with its sign-in flags (a remote GPU box, a
    self-hosted server, an air-gapped paste) and, until it is deleted, `probe
    login`. `device=False` saves the endpoint without minting a token.
    """
    from probe.cli.wizard.account.device_prompt import _show_device_prompt
    from probe.cli.wizard.account.website_onboarding import _finish_website_onboarding
    from probe.core import events as json_events

    resolved_token = token
    base = base_url or _conn.base_url
    signing_in = {"signed_in": bool(device or token)}

    if device and not resolved_token:
        endpoint = resolve(base_url=base).base_url
        print(f"opening {endpoint} for browser approval…" if open_browser
              else f"approve this device at {endpoint}…")

        json_events.step(json_events.Step.SIGN_IN, json_events.Status.STARTED)
        try:
            resolved_token = device_login(endpoint, on_prompt=_show_device_prompt, open_browser=open_browser)
        except OnboardingRequired as exc:
            json_events.step(json_events.Step.SIGN_IN, json_events.Status.FAILED, str(exc))
            _finish_website_onboarding(exc)
        except DeviceLoginError as exc:
            print(f"device login failed: {exc}", file=sys.stderr)
            json_events.step(json_events.Step.SIGN_IN, json_events.Status.FAILED, str(exc))
            json_events.agent_result(
                None, requested=signing_in, actual={"signed_in": False}, ok=False,
                message=f"device login failed: {exc}",
            )
            raise typer.Exit(1) from exc
        json_events.step(json_events.Step.SIGN_IN, json_events.Status.DONE)

    settings = resolve(
        base_url=base,
        token=resolved_token,
        ingest_token=ingest_token,
        hmac_secret=hmac_secret,
        context=context,
    )
    # None means "leave whatever is already there" in save_context, so an --endpoint-only
    # login never clears a token the user still has.
    updates = {
        "base_url": settings.base_url,
        "token": settings.token or None,
        "ingest_token": settings.ingest_token or None,
        "hmac_secret": settings.hmac_secret or None,
    }
    if settings.token:
        with _new_client(settings=settings) as c:
            who = c.me()
        print(f"logged in to {settings.base_url} as {who.get('email', who)}")
        # Which account this login is, bound to its token (#2041 review): a
        # write queued under it may later go out with a NEWER login of this
        # context only if that login is the same account. None clears a
        # previous login's record.
        from ....sdk.delivery.outbox.drain.credentials import credential_fingerprint
        from ....sdk.delivery.outbox.drain.accounts import record_account

        # The login this one replaces keeps its record where writes queued under
        # it can still find it (#2041 round 3): the context holds one identity.
        before = load_context(context)
        previous = before.get("identity")
        if isinstance(previous, dict) and previous.get("fingerprint"):
            record_account(
                str(previous["fingerprint"]),
                (previous.get("customer_id"), previous.get("user_id")),
                # It was this context's login: a job holding a copy of it in
                # PROBE_TOKEN is taken for the login (`Client._is_the_login`).
                login_of=before.get("base_url") or DEFAULT_BASE_URL,
            )
        if isinstance(who, dict) and who.get("customer_id") and who.get("user_id"):
            record_account(
                credential_fingerprint(settings.token, settings.ingest_token),
                (str(who["customer_id"]), str(who["user_id"])),
                login_of=settings.base_url,
            )
        updates["identity"] = (
            {
                "fingerprint": credential_fingerprint(settings.token, settings.ingest_token),
                "customer_id": str(who["customer_id"]),
                "user_id": str(who["user_id"]),
            }
            if isinstance(who, dict) and who.get("customer_id") and who.get("user_id")
            else None
        )
    else:
        print(f"saved endpoint {settings.base_url} (no user token set)")
    if context:
        use_context(context)
    path = save_context(updates, name=context)
    print(f"config: {path} (context: {context or current_context_name()})")
    if settings.token:
        _hold_daemon_key(base_url=settings.base_url)
    json_events.agent_result(
        None, requested=signing_in, actual={"signed_in": bool(settings.token)},
        ok=bool(settings.token) == signing_in["signed_in"],
    )
    if settings.token:
        # Fresh credentials un-block the outbox: forget any recorded 401/403
        # and wake the drainer so queued writes deliver without further steps.
        try:
            journal = _journal()
            journal.clear_auth_block()
            _kick_drainer()
        except Exception:  # noqa: BLE001 -- login must not fail on outbox hygiene
            pass


def _hold_daemon_key(*, base_url: str | None = None) -> None:
    """Who is signed in changed (`probe login`, `probe context use`): the
    daemon key held to that sign-in, as an install does (plan
    clean-uninstall-reinstall R-T4). `save_context` merges, so an earlier
    sign-in's key of another team stayed, and the daemon wrote to the old team:
    it is revoked and dropped (approved afresh where someone can). Lines on
    stdout, problems on stderr. Never raises: the sign-in or the switch is done."""
    try:
        from probe.cli.install import identity_check

        report = identity_check.reconcile(base_url=base_url, only_when_needed=True)
    except Exception as exc:  # noqa: BLE001
        print(f"! the daemon key could not be checked against this sign-in ({type(exc).__name__}); "
              "`probe repair` checks it", file=sys.stderr)
        return
    for line in report.lines:
        print(line)
    for line in report.problems:
        print(f"! {line}", file=sys.stderr)


@app.command()
def logout() -> None:
    """Stop imports, revoke the calling token, and clear local config."""
    from probe.cli.wizard.session.run_lock import _wizard_run_lock
    from probe.cli import wizard as wizard
    from probe import analytics as telemetry_mod

    with _wizard_run_lock(command="probe logout"):
        try:
            base_url = resolve(base_url=_conn.base_url).base_url
        except Exception:  # noqa: BLE001 -- sign-out must not depend on telemetry
            base_url = None
        tel = telemetry_mod.TelemetryContext.start(
            via=telemetry_mod.Via.COMMAND, interactive=wizard.interactive(), base_url=base_url
        )
        # Before the token goes, as the wizard's Sign out does (`pin_identity`).
        tel.pin_identity()
        _clear_wizard_imports()
        try:
            with _client() as c:
                c.logout()
            print("token revoked")
        except errors.RosError as exc:
            print(f"revoke skipped ({exc})", file=sys.stderr)
        tel.emit(telemetry_mod.EVENT_WIZARD_SIGNED_OUT, agent_count=0, warnings=0)
        # The ACTIVE context only. Deleting the whole file would sign the user out of every
        # other endpoint they have configured, which is not what "logout" means.
        name = current_context_name()
        clear_context(name)
        print(f"local config cleared (context: {name})")
        # Kimi Code's installed manifests carry the read token as a bearer header:
        # with the config cleared there is none to hold, so they go back to OAuth.
        from probe.shared.harness.harnesses.kimi_code import config as kimi_config

        for line in kimi_config.sync_mcp_bearer():
            print(line)


@app.command()
def whoami() -> None:
    """Show the current principal."""
    with _client() as c:
        _print_json(c.me())


def _clear_wizard_imports() -> None:
    from probe.cli.imports import jobs as import_jobs
    from probe.cli.wizard import terminal as tui

    try:
        import_jobs.clear_all()
    except (import_jobs.JobError, OSError) as exc:
        tui.say(f"Could not clear imports: {exc}")
        raise typer.Exit(1) from exc
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client, _conn, _journal, _kick_drainer, _new_client  # noqa: E402 -- pieces need each other; the front door loads this one first
