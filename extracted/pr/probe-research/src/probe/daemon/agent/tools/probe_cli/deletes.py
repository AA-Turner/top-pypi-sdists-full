"""hold deletes that reach others' data or have no trash; run what bypass mode approved."""

from __future__ import annotations
import inspect
from pathlib import Path

from probe.shared.mailbox import approvals as appr
from probe.shared.command_rules import command_rules as precheck
from probe.daemon.session import scope
from probe.daemon.store.events import scrub


async def _maybe_hold_delete(deps: Deps, parsed: precheck.Parsed, op_id: str, why: str) -> Outcome | None:
    """`delete.others_data`: a delete whose target or anything under it was made by
    another researcher waits for the researcher's yes (D22). Facts from Probe.
    None: it reaches only the daemon's own work, and runs. Anything it cannot
    establish refuses the delete (FAIL CLOSED): it never runs unchecked."""
    from probe.daemon.session import probe_api

    try:
        facts = await deletion_facts(deps, parsed)
    except probe_api.KeyRefused:
        return write_refusal(deps) or NO_LEASE, None
    except Exception as exc:  # noqa: BLE001 -- a delete nobody could check does not run
        return f"not run: could not read what the delete would reach ({type(exc).__name__}: {exc}).", None
    if facts.get("refused"):
        deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *parsed.argv], head=parsed.path,
                             status="not_run", reason=str(facts["refused"]))
        return f"not run: {facts['refused']}", None
    if not facts.get("others"):
        return None
    facts["reason"] = why
    held = {"kind": "probe", "argv": parsed.argv, "op_id": op_id, "cwd": str(deps.cwd)}
    req = _hold(deps, policy="delete.others_data", facts=facts, held=held)
    if req.state == appr.DENIED:
        return _already_no(req), None
    if req.state == appr.APPROVED:
        return await _run_approved(deps, parsed.argv, op_id, head=parsed.path, request=req.id)
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *parsed.argv], head=parsed.path,
                         status="held", reason="reaches another researcher's data", request=req.id)
    return (f"held for the researcher (request {req.id}) - it deletes another researcher's data. It runs if they "
            "say yes."), None


async def deletion_facts(deps: Deps, parsed: precheck.Parsed) -> dict:
    """What the delete would trash, by creator: `DELETE ...?dry_run=true` (S13),
    sent only to a server that declares the trash. Raises `probe_api.Unreachable`
    when Probe could not be asked whether it has one.

    Never None. When the target cannot be read from the command (under the name
    the CLI's parser gives it: `project_id`, `experiment_id`, `run`), when it is
    not a slug or an id, or when the server has no trash, the facts carry
    `refused` and no id: the caller refuses, and a stored yes no longer matches
    them, so it is void."""
    from probe.daemon.session import probe_api

    kind = precheck.CASCADE_DELETES[parsed.path]
    target = precheck.delete_target(parsed)

    def refused(why: str) -> dict:
        return {"id": None, "name": target, "what": kind, "others": {"unknown owner|items": 1}, "count": None,
                "updated_at": None, "refused": why}

    if not target:
        return refused(f"`probe {parsed.path}` names no target the daemon can read, so it can't check what the "
                       "delete reaches.")
    try:
        probe_api.valid_ref(target)
    except probe_api.BadRef as exc:
        return refused(f"{exc}: a delete takes a slug, a uuid or id:<uuid>")
    trash = await _server_has_trash(deps)
    if trash is None:  # not "no trash": the caller tries again later
        raise probe_api.Unreachable(precheck.TRASH_UNKNOWN)
    if not trash:
        return refused(precheck.NO_TRASH)
    if deps.replay is not None:
        return deps.replay.deletion_facts(kind, target)
    try:
        return await probe_api.deletion_preview(deps.probe_env, kind, target,
                                                recursive=bool(parsed.params.get("recursive")))
    except probe_api.KeyRefused:
        _mark_key_refused(deps)
        raise


async def _own_link(deps: Deps, parsed: precheck.Parsed) -> bool | str:
    """Is this `edge remove` of a link THIS researcher's daemon made (lineage
    plan L9, R9)? Then it runs without a question: the daemon revisits its own
    links as the session goes on. True only when Probe says so
    (`probe_api.edge_is_this_daemons`); anything it cannot establish -- a server
    without `GET /v1/edges/{id}`, an unreadable edge, no answer -- is False, and
    the delete asks as every permanent delete does (FAIL CLOSED, like
    `_maybe_hold_delete`). Bypass mode asks nothing anyway, so it reads nothing.
    A str: the stop message, when Probe refused the key."""
    from probe.daemon.session import probe_api

    if parsed.path != "edge remove" or (deps.bypass and deps.mode_known):
        return False
    edge_id = next((v for v in precheck._strings(parsed.params.get("edge_id")) if v.strip()), None)
    if not edge_id:
        return False
    try:
        if deps.replay is not None:
            check = getattr(deps.replay, "edge_is_this_daemons", None)
            answer = check(edge_id) if callable(check) else False
        else:
            answer = probe_api.edge_is_this_daemons(deps.probe_env, edge_id)
        if inspect.isawaitable(answer):
            answer = await answer
        return answer is True  # only a plain yes exempts it
    except probe_api.KeyRefused:
        _mark_key_refused(deps)
        return write_refusal(deps) or NO_LEASE
    except Exception:  # noqa: BLE001 -- an edge nobody could read is asked about
        return False


async def _hold_permanent_delete(deps: Deps, parsed: precheck.Parsed, op_id: str, why: str) -> Outcome:
    """`delete.permanent`: a delete with no trash behind it (an artifact, a note, a
    paper, a view, an edge...) cannot be undone, so it waits for the researcher's
    yes, whoever made what it deletes. Bypass mode runs it at once."""
    auto = deps.bypass and deps.mode_known
    shown = appr.override_command(parsed.argv)
    if len(shown) > appr.COMMAND_CHARS and not auto:
        return (f"not run: the command is {len(shown)} characters - a question shows at most "
                f"{appr.COMMAND_CHARS}."), None
    facts = {"command": shown, "what": precheck.PERMANENT_DELETES[parsed.path], "undo": "cannot be undone",
             "reason": why}
    held = {"kind": "probe", "argv": parsed.argv, "op_id": op_id, "cwd": str(deps.cwd)}
    req = _hold(deps, policy="delete.permanent", facts=facts, held=held)
    if req.state == appr.DENIED:
        return _already_no(req), None
    if req.state == appr.APPROVED:
        return await _run_approved(deps, parsed.argv, op_id, head=parsed.path, request=req.id)
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *parsed.argv], head=parsed.path,
                         status="held", reason="a delete Probe cannot undo", request=req.id)
    return f"held for the researcher (request {req.id}) - this delete can't be undone. It runs if they say yes.", None


async def _run_approved(deps: Deps, argv: list[str], op_id: str, *, head: str, request: str,
                        cwd: Path | None = None) -> Outcome:
    """A held probe command bypass mode approved at once: run, logged as such."""
    result = await _probe_process(deps, argv, op_id, cwd or deps.cwd)
    code, output = result.code, result.output
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *argv], head=head,
                         status=write_status(code, result.stderr), reason=appr.AUTO, output=output, exit_code=code,
                         request=request)
    if write_status(code, result.stderr) == "ran":
        await scope.stamp_argv(deps, argv)
    stop = write_refusal(deps) if deps.key_refused else None
    return f"[{appr.AUTO} · exit {code}]\n{_cap(scrub(output))}" + (f"\n{stop}" if stop else ""), result


def _is_delete(argv: list[str]) -> bool:
    try:
        return precheck.parse(argv).path in precheck.DELETES
    except precheck.ParseError:
        return False
from probe.daemon.agent.tools.probe_cli.probe_cli import Outcome, _server_has_trash  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.process import ProbeResult, _mark_key_refused, _probe_process, write_status  # noqa: E402, F401 -- pieces need each other; ProbeResult resolves `Outcome` hints
from probe.daemon.agent.tools.refusals import NO_LEASE, write_refusal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps, _already_no, _cap, _hold  # noqa: E402 -- pieces need each other; the front door loads this one first
