"""sign this device in through the browser and keep what it mints: account-switch refusal, releasing replaced credentials."""

from __future__ import annotations
from dataclasses import dataclass
from probe.cli.wizard.state.state import TokenSource
from probe.cli.wizard.state.agent_identity import agent_target
from probe.cli.wizard.state.capture_credentials import capture_token_sources
from probe.cli.capture.capture import clear_killswitch


def locally_paired_capture(sources: tuple[str, ...] | list[str] | str) -> list[str]:
    """The agents whose capture credential THIS DEVICE stores, so a sign-in can
    re-pair them under the new account.

    An environment-variable credential is deliberately not one of them: the
    wizard cannot unset a variable in the parent shell, so re-pairing would mint
    a token the environment then shadows -- capture would keep uploading to the
    old account while the run reported it re-paired.
    """
    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    return [
        source
        for source in normalized
        if {TokenSource.PAIRED_FILE, TokenSource.PROBE_CONFIG} & set(capture_token_sources(source))
    ]


def _revoke(token: str, *, base_url: str, what: str) -> list[str]:
    """Release one credential from THIS machine, best-effort, and say which one.

    A credential nobody holds any more is not harmless: it stays valid until it
    expires, and once the local copy is gone the user has nothing left to revoke
    it WITH. Failure is reported, never raised -- being unable to reach the API
    must not stop a sign-out from clearing the disk.

    REPORTS WHAT ACTUALLY HAPPENED, which is the whole reason this is not just a
    revoke any more. The same PAT may be serving another machine, and the server
    detaches rather than revokes in that case; saying "Revoked" there would tell
    the user they had disconnected a laptop that is still working perfectly.

    An older or self-hosted backend answers 204 with no body and revokes
    globally -- it has never heard of the device header. We cannot make that
    server safe from here, so we say what we know rather than claiming a clean
    rotation we cannot prove.
    """
    from probe.sdk import errors
    from probe.sdk.client.client import Client
    from probe.foundation.request_identity.surface import Surface
    from probe.sdk.settings.settings import Settings, resolve

    endpoint = base_url or resolve().base_url
    try:
        with Client(
            settings=Settings(base_url=endpoint, token=token),
            async_writes=False,
            surface=Surface.CLI.value,
        ) as client:
            result = client.logout()
    except (errors.AuthError, errors.NotFoundError):
        # Already gone. On a current backend the EXCHANGE revokes the replaced
        # credential as part of the rotation, so by the time we get here the
        # token no longer authenticates and the server answers 401 -- which maps
        # to AuthError, not NotFoundError. Catching only 404 made every re-run of
        # `probe setup` print "could not release ..." for work that had already
        # succeeded. Both statuses mean the same thing here: nothing to release.
        return []
    except Exception as exc:  # noqa: BLE001 - offline is a message, not a crash
        return [
            f"! could not release {what} ({exc}). "
            "Revoke it in the dashboard under Settings > Connected clients."
        ]
    if not isinstance(result, dict) or "revoked" not in result:
        # No body: a backend that predates device-aware release. It revoked
        # globally, which is what it has always done.
        return [f"Revoked {what}."]
    if result.get("detached") and not result.get("revoked"):
        others = result.get("still_used_by") or []
        named = ", ".join(str(name) for name in others[:3])
        suffix = f" ({named})" if named else ""
        return [
            f"Disconnected {what} from this machine; "
            f"it is still in use on {len(others)} other device"
            f"{'' if len(others) == 1 else 's'}{suffix}."
        ]
    return [f"Revoked {what}."]


def prior_account(caps_by_source: dict) -> str | None:
    """The account this device is CURRENTLY set up for, or None.

    The verified `logged_in_as` when one resolved, and deliberately nothing
    otherwise: a device that is offline, or whose saved token has been revoked,
    cannot have its account NAMED, and a guessed name is worse than no name on
    both of the screens that read this. Absent here therefore means "we cannot
    say", never "there is nobody" -- `saved_accounts()` is what answers whether
    a credential exists at all.
    """
    return next(
        (snapshot.logged_in_as for snapshot in caps_by_source.values() if snapshot.logged_in_as),
        None,
    )


def install_client_context(caps_by_source: dict) -> dict:
    """The display-only context the guided install sends to the approval page.

    `prior_email` is `prior_account` -- the account this device is currently set
    up for, omitted when it could not be resolved (an offline device gets no
    mismatch warning rather than a guessed one). `install: True` is what tells
    the page to stay open after approval and wait for the wizard's completion
    registration. The page treats every field as the CLI's claim; nothing
    authorizes against it.
    """
    prior = prior_account(caps_by_source)
    context: dict = {"install": True}
    if prior:
        context["prior_email"] = prior
    return context


def account_switch_refusal(previous: str) -> list[str]:
    """The headless answer to an install code on a device signed in as someone else.

    Here rather than inline in main.py so the refusal and the test that pins it
    read one string. It names the flag that consents on purpose: a refusal that
    only says no turns a one-flag fix into a support thread.
    """
    return [
        f"! This device is signed in as {previous}, and a website install code signs in "
        "as whoever generated it.",
        "  Redeeming it would replace that account here and release this device's current "
        "credentials, which cannot be undone from this end.",
        "  Re-run with `--yes` to switch accounts anyway, or run `probe wizard` from a "
        "terminal to be asked.",
    ]


def revoke_replaced_token(previous: dict, granted: dict, *, base_url: str) -> list[str]:
    """After a mint replaced this device's credentials, release the old ones.

    The always-browser install re-mints even on a signed-in device, and
    `authorize` only overwrites the LOCAL copy — without this, every re-run
    leaves another live token behind that nobody holds. Same rule `sign_in` has
    always applied: release AFTER the mint (releasing first would leave a
    refused approval with no credentials at all), and only when the token
    actually changed.

    RELEASE, NOT REVOKE, is the change. The old credential is unbound from THIS
    machine and dies only if no other device still holds it, so rotating a PAT
    that a second laptop is also using no longer signs that laptop out. On a
    current backend the exchange has usually revoked it already, which arrives
    here as a 404 and is silently correct.
    """
    if "api" not in granted:
        return []
    lines: list[str] = []
    replaced = str(previous.get("token") or "")
    if replaced and replaced != granted["api"].get("token"):
        lines += _revoke(
            replaced,
            base_url=str(previous.get("base_url") or base_url),
            what="the token this device was using before",
        )
    # The mint replaces the READ token in the same write, and an orphaned
    # read-capable credential is still a credential. Best-effort like the PAT:
    # `_revoke` is a self-logout, and a token that cannot revoke itself gets
    # the dashboard pointer instead of a crash.
    replaced_mcp = str(previous.get("mcp_token") or "")
    minted_mcp = (granted.get("mcp") or {}).get("token")
    if replaced_mcp and replaced_mcp != minted_mcp:
        lines += _revoke(
            replaced_mcp,
            base_url=str(previous.get("base_url") or base_url),
            what="the read-only MCP token this device was using before",
        )
    # KNOWN LIMIT: a capture daemon already running holds its ingest token in
    # memory until its session ends, and replaced capture DEVICE tokens are
    # retired by re-pairing, not here — the same boundary sign_in has.
    return lines


@dataclass(frozen=True)
class SignInResult:
    """Whether this device came out of the flow signed in, and what to print.

    Two fields because neither implies the other: a sign-in that SUCCEEDED can
    still print warnings -- a capture grant the server declined, a previous
    token we could not revoke -- so "does any line look like a failure" is the
    wrong question to ask about whether the credential landed.
    """

    ok: bool
    lines: list[str]


def sign_in(
    *,
    base_url: str,
    sources: tuple[str, ...] | list[str] | str = ("claude_code",),
    on_prompt=None,
    open_browser: bool = True,
    install_code: str | None = None,
    prepare_install: bool = False,
) -> SignInResult:
    """Approve this device in the browser and save what it mints over the active
    account.

    Re-runnable on a machine that is ALREADY signed in, which is the whole point:
    `needs_authorization` skips the browser for a device that holds a credential,
    so before this existed a wrong-account install had no path forward inside the
    wizard at all.

    Capture already paired on the device rides along so it cannot keep uploading
    to the previous account. Wizard entry also prepares capture for unpaired
    sources in this same approval; those credentials remain disabled until the
    install confirmation. An environment-only credential is left to its owner.
    """
    from probe.sdk.settings.settings import current_context_name, load_context

    # The FILE, not `resolve()`: an exported PROBE_TOKEN belongs to whoever
    # exported it (CI, a colleague's shell profile) and is not ours to revoke.
    previous = load_context()
    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    repair = locally_paired_capture(normalized)
    new_capture = (
        [
            source
            for source in normalized
            if not has_source_capture_grant(source, capture_token_sources(source))
        ]
        if prepare_install
        else []
    )
    requested_capture = list(dict.fromkeys([*repair, *new_capture]))
    grants = ["api", "mcp"] + (["capture"] if requested_capture else [])
    from ...install import identity_check, install as install_pipeline

    # A sign-in starts: the OS keeper may come back (R1), and what is queued
    # under the credential this replaces goes BEFORE the exchange, which
    # releases it on the server (plan clean-uninstall-reinstall R-T4, R8).
    install_pipeline.clear_keeper_off()
    drained = identity_check.drain_before_switch() if previous.get("token") else []

    granted, messages = authorize(
        grants,
        base_url=base_url,
        capture_sources=requested_capture or None,
        **({"defer_capture_sources": new_capture} if prepare_install else {}),
        on_prompt=on_prompt,
        open_browser=open_browser,
        **({"install_code": install_code} if install_code is not None else {}),
    )
    messages = [*drained, *messages]
    if "api" not in granted:
        return SignInResult(
            ok=False,
            lines=[
                *messages,
                "! Sign-in did not complete — this device is still using the credentials it had.",
            ],
        )

    if not prepare_install:
        for source in repair:
            # Explicit sign-in restores existing pairings. Wizard entry leaves
            # every capture switch as it was until installation is confirmed.
            with agent_target(source):
                clear_killswitch()

    # The email is a courtesy, not a requirement: an endpoint that answered the
    # approval can still be unreachable a second later, and the credential is
    # already saved by then. Name whoever we can, and say the rest regardless.
    email = account_email(base_url)
    lines = [
        f"Signed in {f'as {email} ' if email else ''}at {base_url} "
        f"(saved account: {current_context_name()}).",
        *messages,
    ]
    replaced = str(previous.get("token") or "")
    if replaced and replaced != granted["api"].get("token"):
        # AFTER the mint, never before: revoking first would leave a refused
        # approval with no credentials at all.
        lines.extend(
            _revoke(
                replaced,
                base_url=str(previous.get("base_url") or base_url),
                what="the token this device was using before",
            )
        )
    if previous.get("companion_token"):
        # The daemon key an earlier sign-in left: it must be this account's
        # (R5: it stayed, and the daemon wrote to the old team).
        held = identity_check.reconcile(base_url=base_url)
        lines.extend(held.lines)
        lines.extend(f"! {problem}" for problem in held.problems)
    return SignInResult(ok=True, lines=lines)
from probe.cli.wizard.account.account import account_email  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.authorize import authorize  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.capture_credentials import has_source_capture_grant  # noqa: E402 -- pieces need each other; the front door loads this one first
