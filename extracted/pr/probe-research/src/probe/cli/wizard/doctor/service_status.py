"""the Probe service's own view: sessions, recorders, what it is doing."""

from __future__ import annotations


#: Sessions, recorders or holds `doctor` lists one by one before it counts the rest.
SERVICE_ROWS_SHOWN = 5


def _short(sid: object) -> str:
    text = str(sid or "?")
    return text if len(text) <= 12 else text[:12] + "…"


def _session_state(session: dict) -> str:
    """What a "Sessions" row says after the mode: nothing for a live session.
    A session in mode off is never `alive` to the service, whatever its agent
    does, so it is "(off)" while its agent runs (`service_calls.live_off`),
    "(ended)" once it does not."""
    from probe.cli.lifecycle import service_calls

    if session.get("alive"):
        return ""
    return " (off)" if service_calls.live_off(session) else " (ended)"


def _recorder_state(recorder: dict) -> str:
    """"recording" only while the recorder holds its session's claim
    (`recording`): a thread alive in its retry wait, or one whose session
    another recorder (its own `tap watch`) holds, records nothing. A tap before
    0.10.5 publishes no claim (null): its thread's life is all there is. A
    session that is off (`off`) is captured by nobody, whatever the claim."""
    if not recorder.get("alive"):
        return "stopped"
    if recorder.get("off") is True:
        # Held: it may hold the session's claim (so an older tap's `tap watch`
        # hands the session over), and records nothing.
        return "not capturing: Probe is off"
    return "not recording" if recorder.get("recording") is False else "recording"


def service_rows(view: dict) -> list[str]:
    """The Probe service's own view (`service_calls.view()`): the "Probe
    service" section. Pure, like `render`."""
    from probe.cli.lifecycle import service_calls
    from probe.cli.lifecycle.service_calls import Reach

    rows = ["Probe service"]
    reach = view.get("reach")
    if reach == Reach.NOT_RUNNING:
        rows.append(_row("Status", f"not running -- {service_calls.STARTS_WITH}"))
        return rows
    if reach == Reach.UNSUPPORTED:
        rows.append(_row("Status", "does not run on this system yet"))
        return rows
    if reach != Reach.ANSWERED:
        rows.append(_row("Status", f"{reach}: {view.get('error') or 'no answer'}"))
        return rows
    started = view.get("started_at")
    since = f", since {service_calls.when(started)}" if started else ""
    rows.append(
        _row("Status", f"{view.get('state') or 'running'} (version {view.get('version') or 'unknown'}, "
                       f"pid {view.get('pid')}{since})")
    )

    def listed(label: str, items: list, text) -> None:
        if not items:
            rows.append(_row(label, "none"))
            return
        for index, item in enumerate(items[:SERVICE_ROWS_SHOWN]):
            rows.append(_row(label if index == 0 else "", text(item)))
        if len(items) > SERVICE_ROWS_SHOWN:
            rows.append(_row("", f"+{len(items) - SERVICE_ROWS_SHOWN} more"))

    sessions = view.get("sessions") or []
    listed(
        "Sessions",
        sessions,
        lambda s: f"{_short(s.get('sid'))} {s.get('harness')} {s.get('mode')}" + _session_state(s),
    )
    listed(
        "Recorded by the service",
        view.get("recorders") or [],
        lambda r: f"{_short(r.get('sid'))} "
        + _recorder_state(r)
        + (f", last {r['last']}" if r.get("last") else "")
        + (f", {r['failures']} restart(s)" if r.get("failures") else ""),
    )
    listed("Hook hosts", view.get("hook_hosts") or [], lambda h: f"{h.get('root')} (pid {h.get('pid')})")
    unreached = view.get("hints_unreached") or []
    if unreached:
        from probe.foundation.harness_registry import harness_registry as registry

        def agent(harness: object) -> str:
            row = registry.get_registry().find(harness) if isinstance(harness, str) else None
            return row.label if row is not None else "the agent"

        # Its deliverer (a hook or extension) loaded before an update is dead or
        # old: a new process loads the current one (`/reload` is not enough on pi).
        listed(
            "Hints not reaching",
            unreached,
            lambda u: f"{_short(u.get('sid'))} ({u.get('missed')} missed, quit {agent(u.get('harness'))} "
            "and resume the session)",
        )
    listed(
        "Runs in flight",
        view.get("runs") or [],
        lambda r: f"{r.get('run')} (pid {r.get('pid')}, since {service_calls.when(r.get('since'))})",
    )
    imports = view.get("imports") or []
    if imports:
        listed(
            "Imports running",
            imports,
            lambda i: f"{_short(i.get('job_id'))} (pid {i.get('pid')}, since {service_calls.when(i.get('since'))})",
        )
    update = view.get("update") or {}
    rows.append(_row("Updates", service_calls.update_text(update)))
    app_text = service_calls.app_update_text(update.get("app"))
    if app_text:
        rows.append(_row("Desktop app", app_text))
    if update.get("deferred_reason"):
        since_text = service_calls.when(update.get("deferred_since") or update.get("deferred_at"))
        rows.append(_row("Update deferred", f"{update['deferred_reason']} (since {since_text})"))
    return rows
from probe.shared.harness.diagnosis import _row  # noqa: E402 -- pieces need each other; the front door loads this one first
