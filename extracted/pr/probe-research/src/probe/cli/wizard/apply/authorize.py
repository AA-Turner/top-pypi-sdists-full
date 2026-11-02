"""one browser approval for everything ticked: the grants a run still needs, run it, persist what it minted and re-point every agent-held read token."""

from __future__ import annotations
import os
from collections.abc import Iterable
from probe.cli.wizard.state.state import (
    Capabilities,
    Capability)
from probe.cli.wizard.state.agent_identity import agent_source
from probe.cli.wizard.state.capture_credentials import (
    capture_token_sources,
    tap_plugin_dir)
from probe.cli.capture.capture import AWAITING_CONFIRMATION


#: What each capability's plugin cannot work without.
#:
#: `api` rides along with tracking because the CLI needs a credential to be useful
#: at all; `mcp` is the separate read-only one so the MCP surface cannot write. A
#: capture-only selection asks for capture alone -- deliberately, so someone who
#: wanted only transcript capture is not handed read/write/delete they never asked
#: for.
#:
#: ONE table, read by both `grants_for` (what to request) and
#: `blocked_by_missing_grants` (what may install once the answer is back). They were
#: two hardcoded lists for about a day, which is exactly long enough for a third
#: grant to be added to one and not the other -- and the failure mode of that skew
#: is an install gated on a credential nobody asked for, or worse, not gated at all.
CAPABILITY_GRANTS: dict[Capability, tuple[str, ...]] = {
    Capability.TRACKING: ("api", "mcp"),
    Capability.CAPTURE: ("capture",),
}

#: The Probe daemon's own credential: `[read, write, delete]` since the trash
#: (0261; `delete` opens only the move-to-trash routes), revocable on its own.
#: Requested when the `daemon` state is chosen (the menu's Defaults row, or
#: `probe companion authorize`), not by a capability, because `daemon` is a
#: position of the tracking-default row rather than a thing that installs. Stored
#: as the context's `companion_token`, where the tap's worker reads it.
COMPANION_GRANT = "companion"


def grants_for(selection: Selection) -> list[str]:
    """The grant set for ONE browser approval."""
    grants: list[str] = []
    for capability, wanted in CAPABILITY_GRANTS.items():
        if selection.as_map()[capability]:
            grants.extend(wanted)
    return grants


def blocked_by_missing_grants(
    capability: Capability, *, needed: list[str], granted: dict
) -> list[str]:
    """The grants this capability requires that the run TRIED and FAILED to get.

    Only grants in `needed` count. A re-run that already holds `api`/`mcp` never
    asks for them again, so they are absent from `granted` for the good reason --
    reading that as failure would refuse to install on every healthy machine.
    """
    return [
        grant
        for grant in CAPABILITY_GRANTS.get(capability, ())
        if grant in needed and grant not in granted
    ]


def needs_authorization(caps: Capabilities, selection: Selection) -> list[str]:
    """The grants this run must actually obtain, skipping ones already held.

    Re-running with everything already working must NOT drag the user through
    another browser approval -- the wizard is a manager as well as an installer,
    and a no-op re-run should be a no-op.
    """
    wanted = grants_for(selection)
    if not wanted:
        return []
    have: set[str] = set()
    if caps.logged_in_as:
        have.add("api")
    if caps.capture_token_sources and caps.capture_credential_valid is not False:
        have.add("capture")
    # Its own signal, never `api`'s: a token pasted into `probe wizard --action
    # login --token` signs in without an MCP token, and folding `mcp` into
    # `api` left that device with no MCP at all (R11).
    # A token the API REFUSED is not held: re-authorizing is the only repair,
    # and without this a revoked token made `probe wizard` a no-op.
    from probe.cli.wizard.state.mcp_checks import mcp_token_rejected

    if caps.mcp_token_held and not mcp_token_rejected():
        have.add("mcp")
    return [grant for grant in wanted if grant not in have]


def headless_needs(needs: list[str]) -> list[str]:
    """`needs_authorization`'s answer for a run nobody is watching. A missing MCP
    token ALONE never holds an install on a browser approval nobody is there to
    give (it polls for up to 10 minutes): the rest installs as it did before, and
    an interactive Install asks for it."""
    return [] if needs == ["mcp"] else needs


def authorize(
    grants: list[str],
    *,
    base_url: str,
    capture_sources: list[str] | None = None,
    defer_capture_sources: Iterable[str] | None = None,
    client_context: dict | None = None,
    on_prompt=None,
    open_browser: bool = True,
    install_code: str | None = None,
    minted: dict | None = None,
    allow_browser_approval: bool = True,
) -> tuple[dict[str, dict], list[str]]:
    """Run ONE browser approval covering everything the user ticked, and persist
    every credential it mints.

    `minted` is an answer already in hand, in the approval exchange's shape
    (`mint_from_sign_in`): no browser, the same persistence.

    This is the step that makes the whole feature true. Computing the grant set
    and then telling the user to go run `probe login` would leave them with a
    PAT and no capture credential -- capture would still be off after a setup
    that said it turned it on.

    All three credentials go into a single `save_context` write: it is one
    locked read-modify-write, so a partial failure cannot leave the config with
    a PAT but no ingest token (which reads as "logged in, capture silently
    off"). `ingest_token` is exactly where the uploader looks.

    Wizard entry passes `defer_capture_sources` for new capture grants: store
    them disabled until installation is confirmed. Existing disabled markers
    are preserved, and a declined authorization writes no marker.
    """
    from probe.sdk.settings.settings import resolve, save_context
    from probe.sdk.settings.device import (
        DeviceLoginError,
        OnboardingRequired,
        capture_credentials_by_source,
        credentials_by_grant,
        device_authorize,
    )

    if not grants:
        return {}, []

    # Recorder callers explicitly forbid device approval. Configure/repair
    # can need capture alone, so the remaining grants cannot identify a switch.
    if minted is None and install_code is None and not allow_browser_approval:
        return {}, ["Couldn't prepare recording with this Mac's saved sign-in. Refresh your account and try again."]

    try:
        source = agent_source()
        requested_sources = list(dict.fromkeys(capture_sources or [source]))
        source_args = {}
        if "capture" in grants:
            source_args = (
                {"capture_source": requested_sources[0]}
                if len(requested_sources) == 1
                else {"capture_sources": requested_sources}
            )
        if minted is None:
            minted = device_authorize(
                base_url,
                grants=grants,
                **source_args,
                client_context=client_context,
                on_prompt=on_prompt,
                open_browser=open_browser,
                **({"install_code": install_code} if install_code is not None else {}),
            )
    except OnboardingRequired:
        raise
    except DeviceLoginError as exc:
        label = "sign-in" if install_code is not None else "browser approval"
        return {}, [f"{label} failed: {exc}"]

    by_grant = credentials_by_grant(minted)
    captures = capture_credentials_by_source(minted)
    raw_capture_entries = [
        entry for entry in (minted.get("grants") or []) if entry.get("grant") == "capture"
    ]
    if (
        len(requested_sources) == 1
        and len(raw_capture_entries) == 1
        and not raw_capture_entries[0].get("capture_source")
    ):
        # A single-source backend predating the response discriminator is still
        # unambiguous because the request carried exactly one source.
        captures = {requested_sources[0]: raw_capture_entries[0]}
    if captures:
        by_grant["capture"] = next(iter(captures.values()))
    messages: list[str] = []

    updates: dict[str, str | None] = {"base_url": resolve(base_url=base_url).base_url}
    if "api" in by_grant:
        updates["token"] = by_grant["api"]["token"]
    if "mcp" in by_grant:
        updates["mcp_token"] = by_grant["mcp"]["token"]
    if COMPANION_GRANT in by_grant:
        updates["companion_token"] = by_grant[COMPANION_GRANT]["token"]
    if "claude_code" in captures:
        updates["ingest_token"] = captures["claude_code"]["token"]

    try:
        if defer_capture_sources is not None:
            deferred = set(defer_capture_sources) & captures.keys()
            if "claude_code" in captures and not capture_token_sources("claude_code"):
                # The new Claude Code token lands in the shared CLI config, which
                # Claude Code's hooks read. Keep it off until the install is
                # confirmed, even if this sign-in did not select it explicitly.
                # No other agent reads that token, so no other agent is deferred.
                deferred.add("claude_code")
            for deferred_source in sorted(deferred):
                state_dir = tap_plugin_dir(deferred_source)
                state_dir.mkdir(parents=True, exist_ok=True)
                marker = state_dir / ".disabled"
                if not marker.exists():
                    marker.write_text(AWAITING_CONFIRMATION)
        # The markers precede every credential write: an installed hook must
        # never observe a new capture token before the install was confirmed.
        save_context(updates)
    except OSError as exc:
        # The mint SUCCEEDED and the disk write did not: without this the
        # wizard died in a traceback while a live token it never stored sat
        # orphaned server-side. Report it as the failure it is — the caller's
        # grant gating then refuses the installs — and name the cleanup.
        return {}, [
            f"! could not save the minted credentials ({exc}).",
            "  Revoke this device's new token under Settings › Connected clients, "
            "fix the config path, and re-run.",
        ]
    if updates.get("token"):
        _record_login_account(updates["base_url"], updates["token"], updates.get("ingest_token"))

    if install_code is not None:
        # The website code explicitly selects this account. An inherited
        # credential must not keep the current wizard (or its subprocesses)
        # using the old account after a successful exchange. Drop only the
        # overrides for credentials we actually saved, in THIS process; the
        # parent shell retains its environment and needs the instruction below.
        overridden = []
        for field, variable in (
            ("token", "PROBE_TOKEN"),
            ("mcp_token", "PROBE_MCP_TOKEN"),
            ("ingest_token", "PROBE_INGEST_TOKEN"),
        ):
            saved = updates.get(field)
            inherited = os.environ.get(variable)
            if saved and inherited and inherited != saved:
                os.environ.pop(variable, None)
                overridden.append(variable)
        if overridden:
            messages.append(
                "This wizard uses the account selected by the website code. "
                f"Run `unset {' '.join(overridden)}` in your shell before future Probe commands."
            )

    # CODEX HOLDS ITS OWN COPY OF THE READ TOKEN, so the mint above is only half
    # the rotation. Claude Code reads the current token at connect time through
    # its headers helper and needs nothing here; Codex has no credential-helper
    # hook, so its token is a STATIC copy in ~/.codex/config.toml. Leaving that
    # copy behind is not merely stale — `revoke_replaced_token` releases the
    # credential it names — so every Codex call 401s while `codex mcp list`
    # still reports `bearer_token` and `probe doctor` stays green.
    #
    # Here rather than in the callers: sign_in and the guided install both mint
    # through this function, and hooking one of them is how the other keeps the
    # dead token. Costs nothing on a machine with no Codex entry —
    # `configured_bearer` returns None from a file read and the sync returns
    # before it shells out to `codex mcp list`.
    if "mcp" in by_grant:
        messages.extend(sync_mcp_token())

    # Every captured source EXCEPT claude_code needs its token written
    # straight into its own tap plugin dir: claude_code alone can fall back to
    # the probe CLI's config.json `ingest_token` (set above), and every other
    # source is excluded from that fallback (tap/config.py::load_token(),
    # capabilities.consumes_cli_capture_token), so its `.token` file is its
    # ONLY path.
    # A loop over `captures`, not a per-source branch: that is what silently
    # left pi's token nowhere on disk once pi became a real capture source --
    # see AGENT_LABELS' docstring for the same failure mode in the
    # confirmation label below.
    for paired_source, credential in captures.items():
        if paired_source == "claude_code":
            continue
        write_paired_capture_token(paired_source, credential["token"], base_url)

    for grant in grants:
        if grant not in by_grant:
            # Approved, but the backend minted nothing for it. Say so rather
            # than reporting a capability that will not work.
            messages.append(
                f"! the server did not return a '{grant}' credential — "
                "that capability is NOT active"
            )
    if "capture" in grants:
        missing_sources = [source for source in requested_sources if source not in captures]
        if missing_sources:
            by_grant.pop("capture", None)
            messages.append(
                "! the server did not return capture credentials for "
                f"{', '.join(missing_sources)} — those agents are NOT active"
            )
        for paired_source, credential in captures.items():
            label = agent_label(paired_source)
            messages.append(
                f"{label} Session capture paired (device {credential.get('device_id', '?')})."
            )
    return by_grant, messages


def _record_login_account(base_url: str | None, token: str, ingest_token: str | None) -> None:
    """Which account the wizard's new login is, as `probe login` records it
    (#2041 round 3): without it, writes queued under this login could not
    follow a later same-account re-login and waited forever. One `/v1/me`,
    5 s, best-effort: the wizard goes on either way."""
    try:
        from probe.sdk.settings.settings import Settings, resolve, save_context
        from probe.sdk.delivery.outbox.drain.credentials import _identity_of, credential_fingerprint
        from probe.sdk.delivery.outbox.drain.accounts import record_account

        who = _identity_of(Settings(base_url=base_url or resolve().base_url, token=token))
        if who is None:
            return
        fingerprint = credential_fingerprint(token, ingest_token)
        record_account(fingerprint, who)
        save_context({"identity": {"fingerprint": fingerprint, "customer_id": who[0], "user_id": who[1]}})
    except Exception:  # noqa: BLE001 -- see docstring
        return


def mcp_token_drifted() -> bool:
    """Any agent-held copy of the read token (Codex's config, Kimi Code's
    installed manifest) differs from the one this device holds."""
    from probe.shared.harness.harnesses.kimi_code import config as kimi_config

    return codex_mcp_token_drifted() or kimi_config.mcp_bearer_drifted()


def sync_mcp_token() -> list[str]:
    """Re-point EVERY agent-held copy of the read token at the current one:
    Codex's config.toml and Kimi Code's installed manifest. The one call every
    token replacement makes (`authorize()`, `probe mcp token set`, the wizard's
    drift repair), so no copy is left answering 401."""
    from probe.shared.harness.harnesses.kimi_code import config as kimi_config

    return [*sync_codex_mcp_token(), *kimi_config.sync_mcp_bearer()]
from probe.cli.wizard.agents import agent_label  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.capture_credentials import write_paired_capture_token  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.wizard import Selection  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.codex.mcp_auth import codex_mcp_token_drifted, sync_codex_mcp_token  # noqa: E402 -- pieces need each other; the front door loads this one first
