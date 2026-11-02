"""server: preflight every context's server, release this device's credentials and retire its rows, with retries."""

from __future__ import annotations

import contextlib
import json
import time

from probe.foundation.compat.compat import StrEnum
#: Transient server failures are tried this many times, this far apart.
SERVER_TRIES = 3
SERVER_RETRY_S = 1.0


# -- server (U-T6) ---------------------------------------------------------------------------


class Released(StrEnum):
    REVOKED = "revoked"
    DETACHED = "detached"
    GONE = "gone"
    REFUSED = "refused"
    TRANSIENT = "transient"
    #: Every key was refused (401): this computer cannot say whether it was retired.
    UNAUTHORIZED = "unauthorized"


def _client(base_url: str, token: str):
    from probe.sdk.client.client import Client
    from probe.sdk.settings.settings import Settings
    from probe.foundation.request_identity.surface import Surface

    return Client(settings=Settings(base_url=base_url, token=token), async_writes=False, surface=Surface.CLI.value)


def _with_retries(call):
    """`call()` with transient failures tried SERVER_TRIES times. Returns
    (Released or None, answer, error)."""
    from probe.cli.install.uninstall import plan as uninstall_plan
    from probe.sdk import errors

    last = None
    for attempt in range(SERVER_TRIES):
        try:
            return None, call(), None
        except (errors.AuthError, errors.NotFoundError) as exc:
            return Released.GONE, None, exc
        except errors.ScopeError as exc:
            return Released.REFUSED, None, exc
        except Exception as exc:  # noqa: BLE001
            last = exc
            if not uninstall_plan.transient(exc):
                return Released.REFUSED, None, exc
            if attempt + 1 < SERVER_TRIES:
                time.sleep(SERVER_RETRY_S * (attempt + 1))
    return Released.TRANSIENT, None, last


def release(token: str, base_url: str) -> tuple[Released, list[str]]:
    """Revoke one API/MCP/daemon credential of this device (`DELETE
    /v1/tokens/current`, device-aware: a key another computer also holds is
    only detached from this one)."""

    def call():
        with _client(base_url, token) as client:
            return client.logout()

    outcome, result, _error = _with_retries(call)
    if outcome is not None:
        return outcome, []
    if isinstance(result, dict) and result.get("detached") and not result.get("revoked"):
        return Released.DETACHED, [str(n) for n in (result.get("still_used_by") or [])]
    return Released.REVOKED, []


def retire(ids: list[str], tokens: list[str], base_url: str) -> tuple[Released, str]:
    """Retire this device's rows with the first key that may (DELETE scope).
    REVOKED: retired now. GONE: the server has nothing live left to retire
    (404), done. TRANSIENT: no answer; the rerun retires first. UNAUTHORIZED:
    every key was refused (401), so nothing here can tell whether the rows were
    retired (an earlier run's lost answer did, and revoked the keys with them):
    the person removes it in the dashboard. REFUSED: a key without the scope."""
    if not ids:
        return Released.GONE, ""
    is_unauthorized = False
    error = ""
    for token in tokens:

        def call(token=token):
            with _client(base_url, token) as client:
                return client.retire_client_installations(ids)

        result, _answer, exc = _with_retries(call)
        if result is None:
            return Released.REVOKED, ""
        if result is Released.TRANSIENT:
            return result, str(exc)
        if result is Released.GONE and getattr(exc, "status", None) == 404:
            return Released.GONE, ""
        if result is Released.GONE:
            is_unauthorized = True  # a refused key: try the next one
        error = str(exc)
    return (Released.UNAUTHORIZED if is_unauthorized else Released.REFUSED), error


def _capture_tokens(run: Run) -> list[tuple[str, str, str]]:
    """(what, token, base_url) for every capture key this device holds: each
    agent's paired `.token` and every context's `ingest_token`."""
    from probe.cli.install.uninstall import agent_traces as uninstall_agents, plan as uninstall_plan

    out = []
    for folder in uninstall_agents.tap_dirs():
        try:
            token = (folder / ".token").read_text(encoding="utf-8").strip()
        except OSError:
            continue
        config = {}
        with contextlib.suppress(OSError, ValueError):
            config = json.loads((folder / ".config").read_text(encoding="utf-8"))
        base = str((config or {}).get("api_base_url") or "").rstrip("/")
        if token:
            out.append((f"the capture key in {folder}", token, base))
    for name, ctx in uninstall_plan.contexts().items():
        if ctx.get("ingest_token"):
            out.append((f"the capture key of account “{name}”", str(ctx["ingest_token"]),
                        uninstall_plan._base_url(ctx)))  # noqa: SLF001
    seen, unique = set(), []
    for item in out:
        if item[1] not in seen:
            seen.add(item[1])
            unique.append(item)
    return unique


def _dashboard_hint(base_url: str | None = None) -> str:
    from probe.sdk.reads.links import dashboard_base_url

    try:
        base = dashboard_base_url(base_url)
    except Exception:  # noqa: BLE001
        base = None
    return f"{base}/settings" if base else "the dashboard's Settings › Connected clients"


def preflight_server(run: Run) -> None:
    """Right before the point of no return: is every context's server
    reachable? Not: refuse (nothing destroyed yet), unless --offline."""
    from probe.cli.install.uninstall import plan as uninstall_plan

    if run.options.offline or (run.plan.get("server") or {}).get("offline"):
        return
    try:
        uninstall_plan.server_ids()
    except uninstall_plan.Offline as exc:
        if run.resumed:
            raise Stop(EXIT_REFUSED, _offline_resumed(exc), Reason.OFFLINE, {"error": str(exc)}) from None
        raise Stop(EXIT_REFUSED, (
            f"probe uninstall: cannot reach Probe's server ({exc}). Nothing was revoked. Try again when online, "
            "or run `probe uninstall --offline` to remove Probe from this computer only."),
            Reason.OFFLINE, {"error": str(exc)}) from None


def _offline_resumed(exc: Exception) -> str:
    return (f"probe uninstall: cannot reach Probe's server ({exc}), so the uninstall cannot be finished yet: "
            "come back online, or run `probe uninstall --offline` to finish locally (then revoke this computer's "
            "keys yourself in the dashboard).")


def _phase_server(run: Run) -> list[str]:
    from probe.cli.install import capy_retire
    from probe.cli.install.uninstall import plan as uninstall_plan
    from probe.cli.wizard.state.capture_credentials import revoke_capture_token
    from probe.core import events

    lines = run.out
    server = run.plan.get("server") or {}
    if run.options.offline or server.get("offline"):
        hint = _dashboard_hint()
        lines.append(f"! offline: nothing was revoked on the server. Revoke this computer's keys in {hint}.")
        _step(events.Step.UNINSTALL_SERVER, events.Status.SKIPPED, f"offline: revoke this computer in {hint}")
        return lines
    transient: list[str] = []
    planned = server.get("contexts") or {}
    held = uninstall_plan.contexts()
    for name in sorted(set(planned) | set(held)):
        context = held.get(name) or {}
        base_url = (planned.get(name) or {}).get("base_url") or uninstall_plan._base_url(context)  # noqa: SLF001
        ids = list((planned.get(name) or {}).get("installation_ids") or [])
        delete_tokens = [str(t) for t in (context.get("companion_token"), context.get("token")) if t]
        if ids and delete_tokens:
            outcome, error = retire(ids, delete_tokens, base_url)
            if outcome is Released.REVOKED:
                lines.append(f"Retired this computer in account “{name}” ({base_url}).")
            elif outcome is Released.TRANSIENT:
                # Its keys stay: the rerun retires with them first.
                transient.append(f"retiring this computer in “{name}” ({error})")
                continue
            elif outcome in (Released.UNAUTHORIZED, Released.REFUSED):
                lines.append(f"! could not retire this computer in “{name}” ({error or 'its keys were refused'}); "
                             f"remove this computer under Settings > Connected clients ({_dashboard_hint(base_url)}).")
        for key, what in (("token", "API token"), ("mcp_token", "read-only MCP token"),
                          ("companion_token", "Probe daemon key")):
            token = context.get(key)
            if not token:
                continue
            outcome, others = release(str(token), base_url)
            label = f"the {what} of account “{name}”"
            if outcome is Released.REVOKED:
                lines.append(f"Revoked {label}.")
            elif outcome is Released.DETACHED:
                lines.append(f"Disconnected {label} from this computer; it stays in use on {len(others)} other "
                             f"device(s){': ' + ', '.join(others[:3]) if others else ''}.")
            elif outcome is Released.TRANSIENT:
                transient.append(f"revoking {label}")
            elif outcome is Released.REFUSED:
                lines.append(f"! could not revoke {label}; revoke it in {_dashboard_hint(base_url)}.")
    for what, token, base in _capture_tokens(run):
        answer = revoke_capture_token(token, base or uninstall_plan._base_url({}))  # noqa: SLF001
        if answer is None:
            transient.append(f"revoking {what}")
        elif answer:
            lines.append(f"Revoked {what}.")
    lines.extend(capy_retire.retire())
    from probe.cli.wizard.account.sign_out import _env_credential_warnings

    lines.extend(_env_credential_warnings())
    if transient:
        _step(events.Step.UNINSTALL_SERVER, events.Status.FAILED, "; ".join(transient))
        raise Stop(EXIT_PARTIAL, (
            "probe uninstall: Probe's server did not answer while " + "; ".join(transient) + ". Run "
            "`probe uninstall` again to finish (or `probe uninstall --offline` to finish locally and revoke the "
            f"rest in {_dashboard_hint()})."))
    _step(events.Step.UNINSTALL_SERVER, events.Status.DONE, "this computer retired, its keys revoked")
    return lines
from probe.cli.install.uninstall.state import Reason, Run, Stop, _step  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.uninstall import EXIT_PARTIAL, EXIT_REFUSED, run  # noqa: E402 -- pieces need each other; the front door loads this one first
