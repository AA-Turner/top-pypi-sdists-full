"""Codex's McpSlot: authorize its hosted MCP, keep its config.toml bearer and workspace-limit headers on the current read token."""

from __future__ import annotations
from urllib.parse import urlparse
from probe.shared.harness.harnesses.codex import config as codex_config
from probe.shared.harness import plugins as plugin_cli
from probe.cli.wizard.state.state import (
    CODEX_MCP_NAME,
    MARKETPLACE)


def _reuse_approval_for_codex_mcp(notes: list[str]) -> bool:
    """Serve Codex the read token the browser approval already minted.

    The approval this run just performed asks for `api` and `mcp` together and
    stores both, so by the time we get here the credential Codex needs is
    already on disk. Sending the user to a second page to mint another one is
    the whole complaint: it is redundant, and it is the step that times out.

    Declines quietly whenever anything is not exactly right -- no token yet, no
    plugin manifest to read the URL from, an unparseable config -- because the
    OAuth flow below still works and a slower install beats a wrong one.
    """
    from probe.sdk.settings.settings import load_context

    try:
        token = (load_context() or {}).get("mcp_token")
    except Exception:  # noqa: BLE001 - a config we cannot read is just "no shortcut"
        token = None
    if not token:
        return False

    url = codex_config.plugin_mcp_url(CODEX_MCP_NAME, marketplace=MARKETPLACE)
    if not url:
        return False

    try:
        written = codex_config.write_mcp_bearer(CODEX_MCP_NAME, url=url, token=token)
    except codex_config.ConfigError as exc:
        notes.append(f"! could not reuse your sign-in for the Codex MCP: {exc}")
        return False

    # Ask Codex, rather than trusting that valid TOML is acceptable TOML --
    # `bearer_token` is the standing proof those are different things. A status
    # we cannot read is the same shape as a config Codex cannot load, so the
    # write goes back rather than being left for the fallback to sit on top of.
    if plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME) != codex_config.BEARER_STATUS:
        codex_config.restore(written)
        notes.append(
            "! Codex did not accept the credential from your sign-in; its config is back as it was."
        )
        return False
    return True


def _same_deployment(mcp_url: str, base_url: str) -> bool:
    """Do a Codex MCP endpoint and an API base URL belong to one deployment?

    NOT a host comparison. Production deliberately splits the two across
    `api.research.prbe.ai` and `mcp.research.prbe.ai`, so equal hosts is the
    wrong test -- it would reject the configuration nearly every user has.
    There is no base_url -> mcp_url derivation anywhere in this codebase to
    borrow instead (the shipped manifests hard-code the endpoint), so the
    reliable signal is the pairing with the SHIPPED DEFAULTS: stock API with
    stock MCP is one deployment, and either half alone crossing to a
    self-hosted counterpart is the case worth refusing.

    KNOWN LIMIT: two self-hosted deployments on one machine are
    indistinguishable here and both read as "not stock", so this returns True.
    Catching that needs a deployment identity we do not record; this covers the
    crossing that involves production, which is the one with a blast radius
    beyond the person who configured it.
    """
    from probe.sdk.settings.settings import DEFAULT_BASE_URL

    mcp_is_stock = urlparse(mcp_url).netloc == urlparse(codex_config.PRODUCTION_MCP_URL).netloc
    api_is_stock = urlparse(base_url).netloc == urlparse(DEFAULT_BASE_URL).netloc
    return mcp_is_stock == api_is_stock


def codex_mcp_token_drifted() -> bool:
    """Is Codex holding a read token this device has already replaced?

    The predicate the wizard schedules its repair on. Deliberately independent
    of `agent_source` and of `codex mcp list`: the first is single-valued on a
    machine running both agents, and the second answers `bearer_token` for a
    dead header, so both report "fine" in the state this exists to catch.

    Two file reads, no subprocess, and False whenever there is nothing to
    compare -- no Codex entry, or no token stored here. Safe to call on every
    wizard run.
    """
    try:
        configured = codex_config.configured_bearer(CODEX_MCP_NAME)
    except Exception:  # noqa: BLE001 - an unreadable config is "nothing to say"
        return False
    if configured is None:
        # No static bearer (OAuth): only the workspace-limit copy can drift.
        return _codex_limit_drifted()
    token = current_mcp_token()
    if not token:
        return False
    return (
        configured != token
        or codex_config.needs_header_migration(CODEX_MCP_NAME)
        or _codex_limit_drifted()
    )


def sync_codex_mcp_token() -> list[str]:
    """Re-point an existing Codex entry at the CURRENT read token.

    Rotating the credential writes a new `mcp_token` and used to leave Codex
    holding the old one. Nothing noticed: `codex mcp list` reports
    `bearer_token` for any header at all, so the health check stayed green while
    every Codex call 401'd.

    THE ROTATORS ARE `authorize()` AND `probe mcp token set`, and nothing else.
    `probe login` is NOT one of them despite what this docstring said for a
    while: it writes base_url/token/ingest_token/hmac_secret and never touches
    `mcp_token` (see `main.py::login`). Naming it here is how a caller comes to
    believe the login path was already covered.

    Only ever UPDATES an entry that already exists. Creating one is an install
    decision -- it needs the plugin's URL and a verification step -- and
    `probe mcp token set` on a machine that never set up Codex must stay a
    no-op.
    """
    if daemon_records("codex"):
        # The daemon profile gives Codex no MCP: `apply_recorder` removed the
        # table, and re-running the wizard must not bring it back.
        return []
    token = current_mcp_token()
    try:
        configured = codex_config.configured_bearer(CODEX_MCP_NAME)
    except Exception:  # noqa: BLE001
        return []
    if configured is None:
        # No static bearer: an install Codex authenticates itself (OAuth), or no
        # entry at all. The workspace limit must still reach the first.
        return _sync_codex_limit_only()
    if not token:
        return []
    # A ROTATION is not the only reason to rewrite. `write_mcp_bearer` replaces
    # the whole table, so a shape change (the agent-session header) reaches an
    # install only when something calls it -- and an install whose token never
    # rotates would otherwise keep the old table forever.
    stale_shape = codex_config.needs_header_migration(CODEX_MCP_NAME)
    # And a third: this computer's workspace limit, copied into the same table,
    # changed (`probe workspace limit`). The copy must follow it, as the bearer does.
    stale_limit = _codex_limit_drifted()
    if configured is None or (configured == token and not stale_shape and not stale_limit):
        return []

    url = codex_config.plugin_mcp_url(CODEX_MCP_NAME, marketplace=MARKETPLACE)
    if not url:
        return []
    # THE TOKEN AND THE URL COME FROM DIFFERENT PLACES, so they can disagree
    # about which deployment they belong to. `write_mcp_bearer` writes both in
    # one table, and Codex then sends this token to that URL on every connect --
    # so a mismatch hands a live read credential to a server it was not minted
    # for. Silent, and now automatic on every sign-in rather than only on
    # `probe mcp token set`.
    if not _same_deployment(url, _context_base_url()):
        return [
            "! Codex's Probe MCP points at a different deployment than this account; "
            "its token was left alone. Run Install Probe again to fix it."
        ]
    try:
        written = codex_config.write_mcp_bearer(CODEX_MCP_NAME, url=url, token=token)
    except codex_config.ConfigError as exc:
        return [f"! Codex is still using the previous read token: {exc}"]
    if plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME) != codex_config.BEARER_STATUS:
        codex_config.restore(written)
        return ["! could not update the Codex MCP token; its config is back as it was."]
    if configured == token and stale_limit and not stale_shape:
        return ["Codex MCP updated to this computer's workspace limit (restart Codex to load it)."]
    if configured == token:
        return ["Codex MCP config updated so agent sessions are identified."]
    return ["Codex MCP updated to your current read token."]


#: Said whenever this computer is limited while Codex reads Probe through the
#: PLUGIN's own MCP declaration (OAuth, no user-level table). A user-level
#: `[mcp_servers.<name>]` table OVERRIDES the plugin's entry rather than merging
#: with it (`codex_config`, verified on codex-cli 0.147.0), so writing one only to
#: carry the limit would drop the OAuth sign-in it rides on. The safe choice is to
#: leave that connection working and unlimited, and to say how to limit it: signed
#: out, the wizard gives Codex this computer's key, with the limit beside it.
CODEX_UNLIMITED_NOTICE = (
    f"! Codex's Probe MCP signs in with its own OAuth login, so this computer's workspace limit "
    f"cannot ride it and Codex still reads the whole team. To limit it: `codex mcp logout "
    f"{CODEX_MCP_NAME}`, then re-run the Probe wizard (`probe wizard`)."
)


def _sync_codex_limit_only() -> list[str]:
    """Bring the workspace-limit headers of a Codex entry with NO static bearer
    (`codex mcp login`) in step with the Probe config: those headers only, the
    rest of the table untouched. Undone when Codex's own view of its login moves.

    With no user-level table at all -- the plugin's own OAuth declaration -- nothing
    is written (it would shadow that sign-in): while limited, CODEX_UNLIMITED_NOTICE."""
    from probe.sdk.settings.workspace_limit import stored_headers

    url = codex_config.plugin_mcp_url(CODEX_MCP_NAME, marketplace=MARKETPLACE)
    if not url or not _same_deployment(url, _context_base_url()):
        # A limit is one deployment's workspace: never sent to another's MCP.
        return []
    if codex_config.configured_limit_headers(CODEX_MCP_NAME) is None:
        return [CODEX_UNLIMITED_NOTICE] if stored_headers() else []
    if not _codex_limit_drifted():
        return []

    before = plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME)
    try:
        written = codex_config.write_limit_headers(CODEX_MCP_NAME, stored_headers())
    except codex_config.ConfigError as exc:
        return [f"! Codex's Probe MCP keeps its previous workspace limit: {exc}"]
    if written.changed and plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME) != before:
        codex_config.restore(written)
        return ["! could not update the Codex MCP's workspace limit; its config is back as it was."]
    return ["Codex MCP updated to this computer's workspace limit (restart Codex to load it)."] if written.changed else []


def _codex_limit_drifted() -> bool:
    """Codex's table carries other workspace-limit headers than the Probe config
    stores now. False when there is nothing to compare."""
    from probe.sdk.settings.workspace_limit import stored_headers

    try:
        configured = codex_config.configured_limit_headers(CODEX_MCP_NAME)
        return configured is not None and configured != stored_headers()
    except Exception:  # noqa: BLE001 - an unreadable config is "nothing to say"
        return False


def apply_codex_mcp_auth() -> list[str]:
    """Authorize the Codex-hosted MCP, reusing this run's approval if it can."""
    status = plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME)
    if status == codex_config.BEARER_STATUS:
        # Authenticated with a header -- but Codex cannot say WHICH token, so a
        # re-run after a rotation has to check rather than assume.
        return sync_codex_mcp_token()
    if status == "o_auth":
        return []

    notes: list[str] = []
    if _reuse_approval_for_codex_mcp(notes):
        return [*notes, "Codex MCP authorized from your Probe sign-in."]

    result = plugin_cli.login_codex_mcp(CODEX_MCP_NAME)
    if not result.ok:
        return [
            *notes,
            f"could not log in to the {CODEX_MCP_NAME} MCP: {result.detail}. "
            f"Run `codex mcp login {CODEX_MCP_NAME}` and then re-run `probe doctor`.",
        ]
    verified = plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME)
    if verified not in {"o_auth", "bearer_token"}:
        return [
            *notes,
            f"! Codex completed the login command but {CODEX_MCP_NAME} still reports "
            f"{verified or 'unknown'}; run `codex mcp login {CODEX_MCP_NAME}` again.",
        ]
    return [*notes, f"Codex MCP logged in ({CODEX_MCP_NAME})."]
from probe.cli.wizard.apply.apply import daemon_records  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.mcp_token import _context_base_url, current_mcp_token  # noqa: E402 -- pieces need each other; the front door loads this one first
