"""sign this device out: revoke and clear its saved credentials, warn about ones still in the shell, finish an uninstall's device half."""

from __future__ import annotations

import contextlib
import os
from probe.shared.harness.harnesses.codex import config as codex_config
from probe.cli.wizard.state.state import CODEX_MCP_NAME
from probe.cli.wizard.state.agent_identity import agent_target
from probe.cli.wizard.state.capture_credentials import capture_token_sources
from probe.cli.capture.capture import OffMode, turn_off


#: Credentials that live in the SHELL, in resolution-priority order. Every one
#: of them outranks the config file (see sdk/config.resolve), so a sign-out that
#: does not name them would be the same lie about the API that capture.py exists
#: to prevent about transcripts: the file is empty, the CLI still authenticates,
#: and nothing on screen said so.
ENV_CREDENTIALS = (
    "PROBE_TOKEN",
    "PROBE_MCP_TOKEN",
    "PROBE_INGEST_TOKEN",
    "PROBE_SERVICE_TOKEN",
)


def _env_credential_warnings() -> list[str]:
    """Name every credential still live in the shell after a sign-out."""
    live = [name for name in ENV_CREDENTIALS if (os.environ.get(name) or "").strip()]
    if not live:
        return []
    one = len(live) == 1
    return [
        f"! {', '.join(live)} {'is' if one else 'are'} still set in your shell and "
        f"{'outranks' if one else 'outrank'} the file this just cleared.",
        f"  This process cannot unset {'it' if one else 'them'} for you — run "
        f"`unset {' '.join(live)}` and remove the line from your shell profile.",
    ]


#: `release_credentials`' words when the saved credentials stayed on disk:
#: the sign-out and Uninstall pages must not say "signed out" then.
CREDENTIALS_NOT_CLEARED = "could not clear the saved credentials"


def release_credentials() -> list[str]:
    """Revoke this device's saved account and clear it off the disk.

    The credential half of BOTH `sign_out` and Uninstall, so the two can never
    drift into releasing different things. It is device-wide, not per agent --
    there is one config file -- which is why a wizard pass that walks several
    coding agents calls it once, after the last of them.

    Everything here is best-effort and ordered so a failure leaves the machine
    better off, never worse: revoke while we still hold the secret, and clear
    the disk even when the network call did not land.
    """
    from probe.sdk.settings.settings import clear_context, current_context_name, load_context

    context = current_context_name()
    stored = load_context()
    # What removed Capy capture left here (its key, credential and timer) goes
    # with the account, not on the old timer's schedule.
    from ...install import capy_retire

    lines: list[str] = capy_retire.retire()

    if stored.get("token"):
        lines.extend(
            _revoke(
                str(stored["token"]),
                base_url=str(stored.get("base_url") or ""),
                what="this device's API token",
            )
        )
    # THE READ TOKEN IS A CREDENTIAL TOO, and sign-out used to walk past it.
    # Only `token` was released here, so `clear_context` below wiped the local
    # copy of `mcp_token` while the credential itself stayed LIVE server-side --
    # and Codex keeps its own copy in ~/.codex/config.toml, which nothing here
    # touched. A machine someone had signed out of therefore kept working
    # read access to the team's research through Codex. Read-only, and still
    # not something "sign out" is allowed to leave behind.
    #
    # The mint path already got this right (`revoke_replaced_token` releases
    # the replaced `mcp_token`); this is the same release on the way out.
    if stored.get("mcp_token"):
        lines.extend(
            _revoke(
                str(stored["mcp_token"]),
                base_url=str(stored.get("base_url") or ""),
                what="this device's read-only MCP token",
            )
        )
    # Then the copy we do not own the lifetime of. Dropping the whole table is
    # what `remove_everything` already does at uninstall, and for the same
    # reason: an entry left pointing at the hosted MCP with a released token
    # reads as installed and answers 401.
    try:
        if codex_config.configured_bearer(CODEX_MCP_NAME):
            codex_config.remove_mcp_server(CODEX_MCP_NAME)
            lines.append("Removed the Codex MCP entry that held this account's read token.")
    except (codex_config.ConfigError, OSError) as exc:
        lines.append(f"! could not clear the Codex MCP entry ({exc}); remove it by hand.")
    # Only the ACTIVE account, like `probe logout`: clearing the file would sign
    # the user out of every other endpoint saved here, which is not what
    # "sign out" means to anyone.
    #
    # Guarded because this also runs on the way out of Uninstall, where a
    # config file too corrupt to rewrite (`ConfigUnreadable`) must not end a
    # removal in a traceback on a machine whose plugins are already gone.
    try:
        clear_context(context)
    except Exception as exc:  # noqa: BLE001 - an unwritable config is a message, not a crash
        lines.append(
            f"! {CREDENTIALS_NOT_CLEARED} ({exc}). "
            "Delete them by hand, or move the config aside to start fresh."
        )
    else:
        lines.append(f"Signed out. The credentials saved here (account: {context}) are cleared.")
    lines.extend(_env_credential_warnings())
    return lines


def sign_out(sources: tuple[str, ...] | list[str] | str = ("claude_code",)) -> list[str]:
    """Clear this device's saved credentials, and stop everything still using them.

    NOT an uninstall: the plugins stay, so signing back in is one screen away.
    What goes is the ACCOUNT -- the API token (revoked server-side too, so it
    cannot outlive the machine that forgot it) and every capture credential that
    would otherwise keep shipping this device's sessions to the account the user
    just left.
    """
    from ...imports import jobs as import_jobs

    import_jobs.clear_all()
    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    lines: list[str] = ["Imports stopped and local import history cleared."]

    # Capture FIRST: it is the half with a running process behind it, and
    # `turn_off` verifies its own postcondition by re-resolving every source.
    # Clearing the config out from under it would leave that verification
    # reading a state nobody set.
    for source in normalized:
        if not capture_token_sources(source):
            continue
        with agent_target(source):
            result = turn_off(OffMode.DISABLE)
        lines.append(f"{agent_label(source)}: {result.summary()}")
        lines.extend(f"! {warning}" for warning in result.warnings)

    lines.extend(release_credentials())
    lines.append("The plugins are still installed. Uninstall Probe removes them.")
    return lines


def finish_removal() -> list[str]:
    """The device half of Uninstall: sign out, then say what survives.

    Uninstall used to stop at the plugins and TELL the user their account was
    still signed in here, pointing them at Settings to revoke the tokens by
    hand. So a reinstall skipped the browser entirely -- `needs_authorization`
    reads a stored token as "already signed in" -- and a machine somebody had
    deliberately removed Probe from kept a live API token, a live read-only MCP
    token, and enough saved state that the wizard could never show it as fresh.

    Runs ONCE per wizard pass, after every selected agent has been torn down and
    has reported its emptied state to the server: that report authenticates with
    the very token this releases, so doing it any earlier turns the last agent's
    registration into a 401 and leaves the dashboard showing a device that is
    gone.
    """
    # The OS keeper (D35) would start the Probe service again: the system stops running it.
    with contextlib.suppress(Exception):
        from probe.service import keeper

        keeper.remove()
    return [
        *release_credentials(),
        "Setting Probe up again will ask you to sign in.",
        "Data already sent to your team stays.",
    ]
from probe.cli.wizard.account.sign_in import _revoke  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.agents import agent_label  # noqa: E402 -- pieces need each other; the front door loads this one first
