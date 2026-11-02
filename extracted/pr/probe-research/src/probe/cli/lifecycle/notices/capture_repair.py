"""Probe staff opened a capture repair: fetch it, write each agent's credential, lift its lock, report back."""

from __future__ import annotations

import contextlib
import dataclasses
import os
import sys
from ....sdk.settings.settings import (
    load_context,
    resolve)
from ....sdk.errors import NotFoundError
#: A staff capture repair (research-os control/073) is fetched at most this often
#: per machine, under its own stamp (`_capture_repair_notice`).
_CAPTURE_REPAIR_EVERY_S = 10 * 60
_CAPTURE_REPAIR_STAMP = "capture-repair-ask"
#: Where the repair's replacement capture credentials are fetched. Every fetch
#: while the request is open mints them again, so a lost answer is a retry.
CAPTURE_REPAIR_PATH = "/v1/client/capture-repair"
#: Where the machine confirms what it applied; the confirmation closes the request.
CAPTURE_REPAIR_APPLIED_PATH = "/v1/client/capture-repair/applied"


def _capture_repair_notice() -> None:
    """Probe staff opened a one-time capture repair for this machine: fetch the
    replacement capture credentials, write them where the wizard's sign-in
    would, lift those agents' `.disabled` locks, and confirm. Never raises;
    prints one stderr line only when capture an agent had turned off resumes.

    WHY. A wizard bug could revoke a capture credential nobody turned off (a
    Settings commit read a sign-in's pending lock as "capture off" and ran the
    full turn-off; Anthrogen, 2026-10-26). A new one normally needs the
    person's browser approval. Staff can instead open a repair for ONE device
    (research-os control/073): the server answers that device's CLI token with
    `X-Probe-Capture-Repair`, whichever of our clients gets the answer leaves
    the mark (`probe.foundation.remote_settings.capture_repair`), and this, before every command,
    acts on it.

    Gates, cheapest first, like `_remote_update_notice`: not a run-scoped
    command (`_UPDATE_HOT_PATH_COMMANDS`: nothing from inside a training loop)
    and not the service, daemon, MCP, update or the wizard
    (`_REMOTE_UPDATE_SKIP_COMMANDS`); a fresh mark; not a child of the Probe
    service nor a command a Probe daemon runs (`PROBE_DAEMON_SESSION`: its key
    is refused, and it would spend every window); a signed-in API token that IS
    the config file's current context (`_repair_identity_is_the_files`: a
    `PROBE_TOKEN` override would fetch for one account and write into another; a
    URL override for the same token is the same account); one try per
    `_CAPTURE_REPAIR_EVERY_S`
    (`_claim_window`). The gates before the window keep the mark and spend
    nothing. Then:

        fetch 200  each credential is written (`setup.write_capture_credential`;
                   Claude Code's stale tap `.token`, which its tap reads first,
                   is replaced too) and that agent's lock removed. A lock the
                   person set AFTER staff asked (`requested_at`), other than a
                   sign-in's pending one, is kept: that agent is `kept_off`,
                   nothing is written for it
        unknown    an agent this CLI cannot capture is `unsupported`: settled,
                   never retried
        confirm    `CAPTURE_REPAIR_APPLIED_PATH` {requested_at, applied, kept_off,
                   unsupported}, per agent: an agent whose write FAILED is left out
                   and stays open on the server, so the next window fetches (and
                   re-mints) only it. `state: cleared` or a 404 (closed or reopened
                   already) clears the mark; `open` or no answer keeps it
        fetch 404  no open repair for this device: the mark goes
        else       the mark stays and the next window tries again

    `capture.repair_applied` says what happened (`applied`, `kept_off`,
    `write_failed`, `env_shadowed`: `PROBE_INGEST_TOKEN` outranks the Claude
    Code credential just written).
    """
    command = _invoked_command()
    if command in _UPDATE_HOT_PATH_COMMANDS or command in _REMOTE_UPDATE_SKIP_COMMANDS:
        return
    try:
        from probe.foundation.remote_settings import capture_repair

        if not capture_repair.fresh():
            return
        from probe.sdk.agent_session import DAEMON_SESSION_ENV
        from probe.foundation.service_api.paths import SERVICE_CHILD_ENV

        if os.environ.get(SERVICE_CHILD_ENV) or os.environ.get(DAEMON_SESSION_ENV):
            return
        settings = resolve(base_url=_conn.base_url)
        if not settings.token or not _repair_identity_is_the_files(settings):
            return
        if not _claim_window(_CAPTURE_REPAIR_STAMP, _CAPTURE_REPAIR_EVERY_S):
            return
        client = _new_client(base_url=_conn.base_url, spool_dir=_conn.spool_dir)
        try:
            try:
                answer = client.transport.post(CAPTURE_REPAIR_PATH, {})
            except NotFoundError:
                capture_repair.clear()
                return
            except Exception:  # noqa: BLE001 -- no answer, a 5xx, a refusal: the next window retries
                return
            credentials = answer.get("credentials") if isinstance(answer, dict) else None
            if not isinstance(credentials, list):
                return
            # Pinned into each tap's `.config`: the config context's own API, never
            # a shell's override (a port-forward exists only in that shell).
            pinned = (load_context().get("base_url") or settings.base_url).rstrip("/")
            applied = _apply_capture_repair(credentials, _repair_requested_at(answer), pinned)
            is_confirmed = False
            if applied.settled():
                # Per agent: what was written, kept off or cannot be captured here
                # is settled; a failed agent stays open on the server, and only it
                # is fetched (re-minted) next window.
                try:
                    settled = client.transport.post(
                        CAPTURE_REPAIR_APPLIED_PATH,
                        {
                            "requested_at": answer.get("requested_at"),
                            "applied": applied.written,
                            "kept_off": applied.kept_off,
                            "unsupported": applied.unsupported,
                        },
                    )
                    is_confirmed = True
                    if isinstance(settled, dict) and settled.get("state") == "cleared":
                        capture_repair.clear()
                except NotFoundError:
                    is_confirmed = True  # closed (or reopened) already: nothing left to confirm
                    capture_repair.clear()
                except Exception:  # noqa: BLE001 -- unconfirmed: the next window fetches again
                    is_confirmed = False
        finally:
            with contextlib.suppress(Exception):
                client.close()
        if applied.resumed:
            from ... import wizard as wizard

            print(
                f"Probe staff restored session capture for {wizard.agent_label(applied.resumed)} on this "
                "machine (a bug had turned it off). Turn it off any time with `probe wizard`.",
                file=sys.stderr,
            )
        from ...wizard.state.capture_credentials import consumes_cli_capture_token, tap_token_env

        # A credential written to the CLI config ranks below its agent's env token.
        shadowed = any(
            consumes_cli_capture_token(source) and os.environ.get(tap_token_env(source))
            for source in applied.written
        )
        outcome = (
            "write_failed" if applied.failed
            else "env_shadowed" if shadowed
            else "kept_off" if applied.kept_off and not applied.written
            else "unsupported" if applied.unsupported and not applied.written
            else "applied"
        )
        from probe import analytics as telemetry_mod

        telemetry_mod.emit_capture_repair_applied(
            sources=applied.written,
            outcome=outcome,
            locks_lifted=applied.lifted,
            base_url=settings.base_url,
            kept_off=applied.kept_off,
            confirmed=is_confirmed,
            unsupported=applied.unsupported,
        )
    except Exception:  # noqa: BLE001 -- the check never breaks the command it runs before
        pass


def _repair_requested_at(answer: dict) -> float | None:
    """The answer's `requested_at` as unix seconds; None when absent or unreadable."""
    import datetime as _dt

    raw = answer.get("requested_at")
    if not isinstance(raw, str):
        return None
    try:
        return _dt.datetime.fromisoformat(raw.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


@dataclasses.dataclass
class _RepairApplied:
    written: list[str] = dataclasses.field(default_factory=list)
    kept_off: list[str] = dataclasses.field(default_factory=list)
    #: Agents whose lock was a turn-off (not a sign-in's pending lock) and is lifted.
    resumed: list[str] = dataclasses.field(default_factory=list)
    #: Agents this CLI cannot capture: settled with the server, never retried.
    unsupported: list[str] = dataclasses.field(default_factory=list)
    lifted: int = 0
    failed: int = 0

    def settled(self) -> bool:
        return bool(self.written or self.kept_off or self.unsupported)


def _apply_capture_repair(credentials: list, requested_at: float | None, base_url: str) -> _RepairApplied:
    """Write each credential and lift its agent's lock, keeping any turn-off set
    after staff asked. An agent this CLI does not know is `unsupported` (settled,
    never retried); a failed write or a lock that cannot be removed is `failed`:
    the caller confirms the rest, and the server keeps only the failed agents
    open, so the next window fetches (and re-mints) only those."""
    from ... import wizard as wizard
    from ...wizard.state.capture_credentials import consumes_cli_capture_token, tap_plugin_dir
    from ...capture.capture import AWAITING_CONFIRMATION

    result = _RepairApplied()
    for item in credentials:
        source = item.get("capture_source") if isinstance(item, dict) else None
        token = item.get("token") if isinstance(item, dict) else None
        if not (isinstance(source, str) and isinstance(token, str) and token):
            continue
        try:
            directory = tap_plugin_dir(source)  # an agent this CLI knows to capture
        except (ValueError, KeyError):
            result.unsupported.append(source)
            continue
        marker = directory / ".disabled"
        try:
            lock = marker.read_text(encoding="utf-8") if marker.exists() else None
            set_at = marker.stat().st_mtime if lock is not None else None
        except OSError:
            result.failed += 1
            continue
        deliberate = lock is not None and lock != AWAITING_CONFIRMATION
        # A turn-off the person made after staff asked stands. Without the
        # request's time there is no telling, so every turn-off stands.
        if deliberate and (requested_at is None or (set_at is not None and set_at > requested_at)):
            result.kept_off.append(source)
            continue
        try:
            wizard.write_capture_credential(source, token, base_url)
            if consumes_cli_capture_token(source) and (directory / ".token").exists():
                # Claude Code's credential went to the CLI config, which its tap reads
                # after its own `.token`: an older pairing's would shadow it.
                wizard.write_paired_capture_token(source, token, base_url)
            if lock is not None:
                marker.unlink(missing_ok=True)
        except (OSError, ValueError, KeyError):
            result.failed += 1
            continue
        result.written.append(source)
        if lock is not None:
            result.lifted += 1
            if deliberate:
                result.resumed.append(source)
    return result
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _conn, _new_client  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.lifecycle import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _REMOTE_UPDATE_SKIP_COMMANDS,
    _UPDATE_HOT_PATH_COMMANDS,
    _claim_window,
    _invoked_command,
    _repair_identity_is_the_files,
)
