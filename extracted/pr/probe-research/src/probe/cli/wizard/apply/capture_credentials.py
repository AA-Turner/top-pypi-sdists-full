"""where an agent's capture credential is written, and pairing one agent (minted from the sign-in, or a fresh approval)."""

from __future__ import annotations
import json
import os
from collections.abc import Iterable
from probe.cli.wizard.state.state import TokenSource
from probe.cli.wizard.state.agent_identity import (
    agent_source,
    agent_target)
from probe.cli.wizard.state.capture_credentials import (
    capture_token_sources,
    consumes_cli_capture_token,
    tap_plugin_dir)


def has_source_capture_grant(source: str, tokens: Iterable[TokenSource]) -> bool:
    """Whether capture has a credential that can belong to this agent.

    `capture_token_sources` already returns only the agent's own sources: the
    shared CLI config token counts for Claude Code alone (it is Claude Code's
    capture token; the server refuses it on every other agent's route).
    """
    del source  # each agent's sources are already its own
    return bool(set(tokens))


def write_paired_capture_token(source: str, token: str, base_url: str) -> None:
    """One agent's capture credential where its tap reads it: `.token` in its
    own tap folder, beside a `.config` pinning the API origin. Every source but
    claude_code, whose credential is the CLI config's `ingest_token`
    (`write_capture_credential`). Shared by the sign-in (`authorize`) and a
    staff capture repair (`probe.cli.lifecycle.notices.capture_repair._capture_repair_notice`), so the two
    cannot disagree about where a token lives. Raises OSError."""
    state_dir = tap_plugin_dir(source)
    state_dir.mkdir(parents=True, exist_ok=True)
    token_path = state_dir / ".token"
    token_temp = state_dir / ".token.tmp"
    # Created 0600 with the secret's first byte, never written then narrowed:
    # under a 022 umask the old write-then-chmod left the plaintext readable by
    # every local user for that moment. A stale temp file from an interrupted
    # write would keep its old mode under O_CREAT, so it goes first and O_EXCL
    # makes the new one ours.
    token_temp.unlink(missing_ok=True)
    fd = os.open(token_temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(token)
    os.replace(token_temp, token_path)

    # The source-bound device grant is an opaque ros_ing token, not the
    # pairing JWT whose `iss` the standalone tap can inspect. Pin the same
    # API origin used for authorization so the unified tap never falls back
    # to a guessed production host (and self-hosted Codex/pi keep working).
    config_path = state_dir / ".config"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        config = {}
    if not isinstance(config, dict):
        config = {}
    config["api_base_url"] = base_url.rstrip("/")
    config_temp = state_dir / ".config.tmp"
    config_temp.write_text(json.dumps(config, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(config_temp, config_path)


def write_capture_credential(source: str, token: str, base_url: str) -> None:
    """Where `authorize` would put one agent's capture credential. claude_code
    (`consumes_cli_capture_token`): the CLI config's `ingest_token` (its hooks
    read that); every other agent: its tap folder's `.token`
    (`write_paired_capture_token`). Raises OSError."""
    if consumes_cli_capture_token(source):
        from probe.sdk.settings.settings import save_context

        save_context({"ingest_token": token})
        return
    write_paired_capture_token(source, token, base_url)


def needs_capture_pairing(source: str) -> bool:
    """A settings-entry daemon profile (pi) whose agent holds no capture token
    of its own yet: the switch pairs it first (`pair_capture`), OUTSIDE the
    switch's spinner, because the approval prints a link to open."""
    from probe.foundation.harness_registry import get_registry

    harness = get_registry().get(source)
    return harness.lean_profile == LEAN_SETTINGS_FILTER and not capture_token_sources(source)


def mint_from_sign_in(grant: str, *, base_url: str, source: str | None = None) -> dict | None:
    """The daemon's key (`COMPANION_GRANT`) or one agent's capture key
    (`"capture"`, with `source`), minted with this device's sign-in -- its
    installation `api` credential -- and no browser (Richard 2026-10-26: "just
    reuse the auth token already signed into").

    Callers mint this way only once a person saw the daemon's consent on this
    run; a run nobody watches keeps the browser approval, which shows it.

    Answers in the approval exchange's shape (`{"grants": [entry]}`), for
    `authorize(..., minted=)` to persist exactly as a browser approval's. None
    when this device cannot: no saved sign-in, a `PROBE_TOKEN` in the
    environment naming another credential (the key would be saved beside the
    wrong account), a sign-in the server will not mint from (not this
    installation's, another machine's, an older server without the route), or
    an answer that is not one. The caller then opens the browser approval as
    before. A send that fails is retried ONCE: each mint frees the slot of the
    key before it, so a key whose answer was lost dies with the retry rather
    than staying live and unheld.
    """
    from probe.sdk import errors
    from probe.sdk.client.client import Client
    from probe.sdk.settings.settings import load_context, resolve
    from probe.foundation.request_identity.surface import Surface

    settings = resolve(base_url=base_url)
    try:
        saved = str((load_context() or {}).get("token") or "")
    except Exception:  # noqa: BLE001 - an unreadable config holds no sign-in
        return None
    inherited = os.environ.get("PROBE_TOKEN")
    if not saved or (inherited and inherited != saved):
        return None
    for _attempt in range(2):
        try:
            with Client(
                base_url=settings.base_url,
                token=saved,
                fail_open=False,
                async_writes=False,
                surface=Surface.CLI.value,
            ) as client:
                entry = (
                    client.mint_capture_credential(source or agent_source())
                    if grant == "capture"
                    else client.mint_companion_credential()
                )
        except (errors.TransportError, errors.ServerError):
            continue
        except (errors.RosError, ValueError):  # a refusal, or a 2xx that is not JSON (a proxy)
            return None
        if isinstance(entry, dict) and entry.get("grant") == grant and entry.get("token"):
            return {"grants": [entry]}
        return None
    return None


def pair_capture(source: str, *, base_url: str, open_browser: bool = True, sign_in: bool = False) -> list[str]:
    """This agent's capture key alone (nothing else is re-minted): from this
    device's sign-in when `sign_in` (the caller showed the daemon's consent;
    `mint_from_sign_in`), else one browser approval. The person chose the
    daemon, which records from capture, so a leftover sign-in marker in the
    agent's folder goes too."""
    from probe.cli.wizard.state.agent_identity import agent_target
    from probe.cli.capture.capture import clear_stray_pi_killswitch
    from probe.analytics.analytics import DESKTOP_HUMAN_ENV

    desktop = os.environ.get(DESKTOP_HUMAN_ENV) == "1"

    label = agent_label(source)
    lines = [f"Pairing {label}'s session capture (the daemon records from it)."]
    try:
        _grants, messages = authorize(
            ["capture"],
            base_url=base_url,
            capture_sources=[source],
            open_browser=open_browser,
            minted=mint_from_sign_in("capture", base_url=base_url, source=source) if sign_in or desktop else None,
            allow_browser_approval=not desktop,
        )
        lines.extend(messages)
    except Exception as exc:  # noqa: BLE001 - every failure reads as "not paired" in apply_recorder
        lines.append(f"! pairing {label}'s capture did not finish: {exc}")
        return lines
    if capture_token_sources(source):
        with agent_target(source):
            clear_stray_pi_killswitch()
        lines.append(f"{label} capture paired.")
    return lines
from probe.cli.wizard.account.sign_in import sign_in  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.agents import agent_label  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.authorize import authorize  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.recorder import LEAN_SETTINGS_FILTER  # noqa: E402 -- pieces need each other; the front door loads this one first
