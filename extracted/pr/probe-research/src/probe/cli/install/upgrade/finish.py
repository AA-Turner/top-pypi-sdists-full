"""record each agent's pass: doctor's attempt line, the server's update report, a crashed or overdue pass as its failure."""

from __future__ import annotations
import time
from collections.abc import Callable

from probe import __version__
# `update_report` is imported HERE, at the top, for the same reason updater.py
# imports its whole call graph eagerly (H8): it runs after `uv tool upgrade` has
# replaced the installed tree, when a first import would read the new files.
from probe.shared.updates import autoupdate
from probe.cli.install import updater
from probe.shared.updates import update_report
from probe.foundation.harness_registry import get_registry
from probe.core import events as json_events


def _crashed_pass(
    source: str,
    exc: BaseException,
    lines: list[str],
    *,
    prelude: "_Prelude",
    base_url: str,
    trigger: update_report.Trigger,
) -> UpdateOutcome:
    """One agent's pass that raised or ran out of time (`_plugin_passes`): recorded
    and reported as that agent's failure (`_record_crash`), answered like the rest."""
    detail = _stopped_detail(_plugins_of(source), exc)
    _record_crash(source, exc, prelude=prelude, base_url=base_url, trigger=trigger, detail=detail)
    result = prelude.res
    heading = f"{_agent_label(source) or source} plugins:"
    return UpdateOutcome(
        lines=[*lines, heading, f"  ! {detail}"],
        ok=False,
        restart_needed=False,
        problems=[detail],
        run_notes=[*([f"Probe CLI: {result.message}"] if result is not None and not result.ok else [])],
        cli=_cli_line(result),
    )


def _cli_from(res: "updater.CliResult | None") -> str:
    """The CLI version this update started from: the hand-off's (the version
    before this release took the update over, `adopt.cli_result`), else this one."""
    from probe.core import adopt

    return (res.before if res is not None and res.before and adopt.adopted_from() else None) or __version__


def _cli_line(res: "updater.CliResult | None") -> str:
    """"Probe CLI 0.324.0 (updated from 0.323.1)": the CLI's version line."""
    if res is None:
        return f"Probe CLI {__version__}"
    return f"Probe CLI {res.after or __version__}" + (
        f" (updated from {res.before})" if res.changed and res.before else ""
    )


def _finish_pass(
    agent: _AgentPass,
    lines: list[str],
    *,
    prelude: _Prelude,
    include_plugin: bool,
    base_url: str,
    trigger: update_report.Trigger,
) -> UpdateOutcome:
    """One agent's pass recorded (`probe doctor`'s attempt, the server's report)
    and answered, from the run's `prelude` and the agent's own `agent` pass."""
    source, pres, tap_behind = agent.source, agent.pres, agent.tap_behind
    nothing_installed = agent.nothing_installed
    result, refused, pi_update = prelude.res, prelude.refused, prelude.pi_update
    cli_target, plugin_target, tap_target = prelude.cli_target, prelude.plugin_target, prelude.tap_target

    # `attempted` is what separates "the plugin update failed" from "there was no
    # Claude Code to update" -- a CLI-only user has no `claude` on PATH, and
    # recording that as a failure every session would train everyone to ignore
    # the one line that is supposed to mean something. `nothing_installed` is
    # the same for an agent that IS here with no Probe plugin in it: its update
    # command fails because there is nothing to update.
    #
    # A tap still behind the manifest after the run fails the plugin half too:
    # it is installed, `claude` was asked to move it, and it did not. So does a
    # tap the run removed (`tap_verdict`).
    #
    # EVERY way this half fails has a component in the server's report that
    # says so (`update_report`'s rules read the same facts); a pass that failed
    # with every component reading fine is what this used to send.
    is_plugin_ok = (
        True if pres is None else (pres.confirmed or not pres.attempted or nothing_installed)
    ) and not tap_behind
    if pres is not None and not pres.confirmed and not nothing_installed:
        plugin_detail = pres.message
    else:
        # Sessions on an older tap are not a failure, but `probe doctor` is
        # where a person looks, so the local record says it too.
        plugin_detail = tap_behind or (updater.running_stale_note(pres) if pres else "")
    # pi's package is the plugin half for pi: an attempted update that failed
    # fails it, or a detached run (pi's session start) would report success.
    if pi_update is not None and not pi_update.ok:
        is_plugin_ok = False
        plugin_detail = "; ".join(part for part in (plugin_detail, pi_update.detail) if part)
    plugin_version = pres.after if pres is not None else None
    json_events.step(
        json_events.Step.UPDATE_INTEGRATIONS,
        json_events.Status.DONE if is_plugin_ok else json_events.Status.FAILED,
    )
    json_events.step(json_events.Step.VERIFY_UPDATE, json_events.Status.STARTED)

    # The ONLY way a detached auto-update can report failure: it runs with no
    # terminal attached, so without this an updater that has been broken for a
    # month is indistinguishable from one that works. `probe doctor` prints it.
    # BOTH halves are recorded -- the plugin's outcome used to live only in
    # `lines`, which a detached run sends straight to /dev/null.
    attempted_at = int(time.time())
    autoupdate.record_attempt(
        autoupdate.Attempt(
            at=attempted_at,
            # No `res` means the install method was one we refuse to auto-upgrade.
            # That is a deliberate skip, not a failure.
            ok=result.ok if result is not None else True,
            detail="" if result is None or result.ok else result.message,
            # The version the machine ran before: a hand-off's (`adopt.cli_result`)
            # when this release took the update over, else this one.
            from_version=_cli_from(result),
            # A failure with no observed version records none: falling back to
            # the manifest's latest printed "FAILED ... still at CLI <latest>".
            to_version=(
                cli_target if result is None else result.after or (cli_target if result.ok else None)
            ),
            plugin_ok=is_plugin_ok,
            plugin_detail=plugin_detail,
            plugin_version=plugin_version,
        ),
        agent=_agent_label(source),
    )
    ok = (result.ok if result is not None else True) and is_plugin_ok

    # The same outcome, to the server, per component -- the local record above
    # is read by `probe doctor` on THIS machine only. Best-effort and bounded;
    # see update_report.
    _report_attempt(
        lambda: update_report.attempt_report(
            trigger=trigger,
            ok=ok,
            at=attempted_at,
            source=source,
            cli=update_report.cli_component(
                result, current=__version__, target=cli_target, refused=refused
            ),
            # No marketplace plugin ran (`pres`) although plugins were asked
            # for: pi, whose package IS its plugin half. On another agent's
            # pass pi's package moves too, and its failure fails the pass, so
            # it is named there as well (`plugin_half`).
            plugin=(
                update_report.pi_component(pi_update, target=plugin_target)
                if include_plugin and pres is None
                else update_report.plugin_half(
                    update_report.plugin_component(pres, target=plugin_target, source=source),
                    update_report.pi_component(
                        pi_update, target=plugin_target, harness=_package_harness()
                    )
                    if pi_update is not None and not pi_update.ok
                    else None,
                )
            ),
            tap=update_report.tap_component(pres, target=tap_target),
            legacy_ids=pres.legacy_ids if pres is not None else (),
        ),
        base_url=base_url,
    )

    json_events.step(json_events.Step.VERIFY_UPDATE, json_events.Status.DONE)
    summary, problems, actions = agent.summary, list(agent.problems), list(agent.actions)
    pi_failure = ""
    if pi_update is not None and not pi_update.ok:
        # Its own line under "pi package:", which carries the command to run.
        said = [line.strip().removeprefix("! ").strip() for line in pi_update.lines[1:] if line.strip()]
        pi_failure = f"pi's Probe package: {said[0] if said else pi_update.detail}"
    pi_action = pi_update.action if pi_update is not None else ""
    if source == _package_harness() and pi_update is not None:
        if pi_update.ok and pi_update.after:
            moved = pi_update.ran and pi_update.before not in (None, pi_update.after)
            summary = f"package {pi_update.after}{' (updated)' if moved else ''}"
        problems += [pi_failure] if pi_failure else []
        actions += [pi_action] if pi_action else []
    return UpdateOutcome(
        lines=lines,
        # Both halves, so `probe update`'s exit code means "the update worked",
        # not "the CLI half worked".
        ok=ok,
        restart_needed=agent.restart_needed,
        plugins_moved=agent.plugins_moved,
        summary=summary,
        problems=problems,
        actions=actions,
        # pi's package moves whatever agents run (`_update_pi_package`): its
        # failure (and what its sessions must do: `run_actions`) is the run's,
        # and pi's own where pi is one of them (the summary names each once).
        run_notes=[
            *([f"Probe CLI: {result.message}"] if result is not None and not result.ok else []),
            *([pi_failure] if pi_failure else []),
        ],
        run_actions=[pi_action] if pi_action else [],
        cli=(
            f"Probe CLI {result.after or __version__}"
            + (f" (updated from {result.before})" if result.changed and result.before else "")
            if result is not None
            else f"Probe CLI {__version__}"
        ),
    )


def _record_crash(
    source: str,
    exc: BaseException,
    *,
    prelude: _Prelude,
    base_url: str,
    trigger: update_report.Trigger,
    detail: str | None = None,
) -> None:
    """A pass that raised (or ran out of time), recorded as the failure it is
    (`probe doctor`'s attempt, the server's report). The run's one merged
    record reads only what its passes recorded, so without this an Update
    whose Codex pass crashed beside a Claude Code pass that worked said ok.
    Never raises."""
    result, cli_target = prelude.res, prelude.cli_target
    detail = detail or f"the update stopped: {type(exc).__name__}: {exc}"
    at = int(time.time())
    try:
        autoupdate.record_attempt(
            autoupdate.Attempt(
                at=at,
                ok=result.ok if result is not None else True,
                detail="" if result is None or result.ok else result.message,
                from_version=_cli_from(result),
                to_version=cli_target if result is None else result.after or (cli_target if result.ok else None),
                plugin_ok=False,
                plugin_detail=detail,
            ),
            agent=_agent_label(source),
        )
    except Exception:  # noqa: BLE001 - the error itself still rises
        pass
    _report_attempt(
        lambda: update_report.attempt_report(
            trigger=trigger,
            ok=False,
            at=at,
            source=source,
            cli=update_report.cli_component(result, current=__version__, target=cli_target, refused=prelude.refused),
            plugin=update_report.error_component(detail, target=prelude.plugin_target),
            tap=None,
        ),
        base_url=base_url,
    )


def _agent_label(source: str | None) -> str | None:
    """The coding agent a pass ran for, as `probe doctor` names it."""
    try:
        return get_registry().get(source).label if source else None
    except Exception:  # noqa: BLE001 - only a label
        return source


def _report_attempt(build: Callable[[], dict], *, base_url: str | None = None) -> None:
    """Build the server's update report and send it. NEVER RAISES.

    By the time this runs the update is over and recorded locally (`probe
    doctor` reads that record). A bug in building or sending the report may
    cost the report; it must never turn a finished update into a traceback."""
    try:
        update_report.submit_attempt(build(), base_url=base_url)
    except Exception:  # noqa: BLE001 - see docstring
        pass
from probe.cli.install.upgrade.components import _stopped_detail  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.package_step import _package_harness  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.plugin_pass import _AgentPass, _plugins_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.prelude import _Prelude  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.upgrade import UpdateOutcome  # noqa: E402 -- pieces need each other; the front door loads this one first
