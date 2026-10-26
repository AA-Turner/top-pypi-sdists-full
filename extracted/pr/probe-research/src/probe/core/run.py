"""`python -m probe.core.run <action>`: one Probe action, as a child process.

The Probe service runs every action this way (plan R9: the event stream owns
the process's stdout, which a server cannot give one request), and the
desktop app can too. The contract is `probe wizard --json`'s:

    argv    one action: configure | recorder | logout | uninstall | update |
            session_default | workspace_limit | status | version | report | desktop.
            Spawn it as `<python> -I -m
            probe.core.run <action>` from a directory of its own: `-m` puts
            the working directory first on `sys.path`, so a `probe/` folder or
            a `json.py` there would run instead (`-I` keeps it off).
    stdin   one JSON object, UTF-8, the action's params (Probe service API v1
            `action.run` params; `probe.core.requests`). Empty means {}. It is
            read to its end: close it after the request.
    stdout  NDJSON events, schema v1 (`probe.core.events`), `done` last however
            the run ends: the same events `probe wizard --action <a> --yes
            --json` writes for the same request. `status` is a read, not an
            action: it writes `probe status --json`'s one object instead, and
            `version` writes `{"cli_version": "<the installed CLI's>", "cli_latest":
            "<the newest release, or null>"}` (`{"latest": true}`: asked of the
            manifest itself, adding `"reachable"`, false when it got no HTTP
            answer at all, else the cached manifest; `{"refresh": true}`:
            the cached manifest refreshed first, as the CLI's own refresher
            does, adding `"ok"` and `"fetched_at"`). `report` is a read too:
            one diagnostic report to the Probe team (`probe.core.report`;
            params `{"auto", "family", "reason", "sid", "env", "facts"}`),
            writing `{"sent", "id", "skipped", "path"}`. `desktop` reads one
            desktop management request (`probe desktop request --json`'s
            stdin) and writes that command's v1 envelope, with its exit status
            (the Probe service's `desktop.request`).
    stderr  everything else: the run's own text and its child processes'.
    exit    0 done, 1 failed, 2 usage (an unknown action or a request it
            refuses: `error{code: usage}` + `done`), 75 another setup holds
            the lock, 130 interrupted during a browser approval (SIGINT),
            128+N stopped by signal N (SIGTERM, SIGHUP).

It runs the action and nothing else `probe` does around a command: no version
nudge or auto-update spawn, no outbox banner, no capture heal (the root
callback's every-command notices). The harness session is looked up as `probe`
looks it up, so a coding agent's own shell is refused what `probe` and its
guard refuse it: `session_default` by `probe session default`'s own check, and
every wizard action from inside a session the Probe daemon records
(`actions._refuse_from_daemon_session`).
"""

from __future__ import annotations

import sys
from typing import TextIO

from probe.core.requests import ActionName

USAGE = (
    "usage: python -I -m probe.core.run <action> < request.json\n"
    f"  actions: {', '.join(action.value for action in ActionName)}"
)


def main(argv: list[str] | None = None, stdin: TextIO | None = None) -> int:
    """Run one action; returns the exit status (never calls sys.exit itself)."""
    from probe.core import requests

    args = list(sys.argv[1:] if argv is None else argv)
    try:
        if len(args) != 1 or args[0].startswith("-"):
            raise requests.RequestError(f"expected exactly one action, got {args!r}\n{USAGE}")
        action = requests.action_name(args[0])
        if action is requests.ActionName.DESKTOP:
            return _desktop(sys.stdin if stdin is None else stdin)
        request = requests.parse_json(action, _request_text(action, sys.stdin if stdin is None else stdin))
    except requests.RequestError as exc:
        return _usage_error(str(exc))

    if action is requests.ActionName.VERSION:
        # What this process imported: after `uv tool upgrade`, the new files.
        import json

        from probe import __version__

        refreshed = _refresh_manifest() if request.refresh else {}
        latest, reachable = _cli_latest(fetch=request.latest)
        answer = {"cli_version": __version__, "cli_latest": latest, **refreshed}
        if request.latest:
            answer["reachable"] = reachable
        sys.stdout.write(json.dumps(answer) + "\n")
        return 0

    from probe.sdk import agent_session

    refused = _caller_session_refusal(action)
    if refused is not None:
        return _usage_error(refused)
    try:
        if action is requests.ActionName.REPORT:
            # The service's child: the session is the request's `sid`, never one
            # found by walking this process's ancestors.
            agent_session.forgo_harness_process_session()
            return _report(request)
        if action is requests.ActionName.STATUS:
            # As `probe status`: it reads no session, so it walks no ancestors (`ps`).
            agent_session.forgo_harness_process_session()
            from probe.core import reads

            reads.print_status(refresh=request.refresh)
            return 0
        # As `probe` does before any other command: a harness that names no session
        # in its shells (Kimi Code) is found from its process, so the refusals that
        # read the session (`probe session default` from an agent) still hold.
        agent_session.adopt_harness_process_session()
        return _dispatch(action, request)
    except Exception as exc:
        # A bug: its `error` and `done` are written. Report it, then re-raise for
        # the traceback, exactly as `probe` does (`probe.cli.main.main`).
        from probe._shared import telemetry as telemetry_mod

        telemetry_mod.report_crash(exc, surface="cli")
        raise


#: The actions that read rather than change: the caller's session is not
#: looked up for them (`_caller_session_refusal`).
READS = frozenset({ActionName.REPORT, ActionName.STATUS, ActionName.VERSION})


def _caller_session_refusal(action) -> str | None:
    """The Probe service names the process that asked for an action
    (`management.CALLER_PID_ENV`, #3360): when this child's environment names
    no agent session, the CALLER's own one joins it, resolved from that
    process as its own `probe` would (`agent_session.session_env_of_process`:
    its environment, a harness-process marker above it), registered with the
    service or not. So `_refuse_from_daemon_session` and `probe session
    default`'s own check hold for a caller whose session's registration was
    ended or replaced, as `desktop`'s gate does (`_desktop_refusal`). A caller
    that has exited since cannot be checked: refused. The variables are
    removed either way (a later child never inherits them)."""
    import os

    from probe.sdk import agent_session
    from probe.service import management, procid

    caller = os.environ.pop(management.CALLER_PID_ENV, "")
    started = os.environ.pop(management.CALLER_START_ENV, "")
    if action in READS or not caller.isdigit():
        return None
    if started and procid.alive(int(caller), started) is False:
        return "the process that asked has exited, so the session it runs in cannot be checked; ask again"
    if agent_session.session_id_from_env(os.environ):
        return None  # the request's context, or the service, named it already
    os.environ.update(agent_session.session_env_of_process(int(caller)))
    return None


def _report(request) -> int:
    """`report`: one diagnostic report, its answer as ONE object on the real
    stdout. Whatever the collectors print goes to stderr meanwhile."""
    import json

    from probe.core import events, report

    with events.redirect_stdout() as out:
        answer = report.run(request)
        out.write(json.dumps(answer.as_json()) + "\n")
    return 0


#: The command `desktop` answers for, as the CLI's gates read it.
DESKTOP_ARGV = ("desktop", "request", "--json")


def _desktop_refusal() -> str | None:
    """The CLI's own gate for `probe desktop request --json` (`write_gate`),
    before anything reads an account, a transcript or a job: what `probe`
    refuses in a session the daemon records (or one switched off) is refused
    here, by the session's saved policy, registered with the service or not.
    Two sessions are gated: the one this child's environment names (the
    request's context, or the registered session the service handed on), and
    the one the CALLER runs in, resolved from its process exactly as its own
    `probe` would (`agent_session.session_env_of_process`: its environment, a
    harness-process marker above it, the CLI's precedence), the service having
    named that process (`management.CALLER_PID_ENV`). A caller that has
    exited since cannot be checked: refused."""
    import os

    from probe.cli import write_gate
    from probe.sdk import agent_session
    from probe.service import management, procid

    caller = os.environ.pop(management.CALLER_PID_ENV, "")
    started = os.environ.pop(management.CALLER_START_ENV, "")
    excluded = write_gate.excluded_refusal(DESKTOP_ARGV)
    if excluded is not None:
        return excluded[0]
    refused = write_gate.refusal(DESKTOP_ARGV, directed=False)
    if refused or not caller.isdigit():
        return refused
    if started and procid.alive(int(caller), started) is False:
        return "The process that asked has exited, so the session it runs in cannot be checked; ask again."
    peer = agent_session.session_env_of_process(int(caller))
    if not peer:
        return None
    return write_gate.refusal(DESKTOP_ARGV, directed=False, env=peer)


def _desktop(source: TextIO | None) -> int:
    """`desktop`: one management request on stdin, its v1 envelope on stdout,
    and the exit status, exactly as `probe desktop request --json` (both are
    `probe.cli.desktop.respond`), for the Probe service's `desktop.request`.
    Whatever else the request's code prints goes to stderr: stdout is the
    envelope alone. Like `probe desktop` (a read-only command), it walks no
    process ancestry of its own for a session (its parent is the service; the
    caller's is walked instead, `_desktop_refusal`); and like every `probe` command
    (`probe._entry`), it waits out an update's barrier before it imports the
    CLI, else answers busy (exit 75) with nothing loaded from replaced files."""
    import json

    from probe.service import barrier

    if not barrier.wait():
        sys.stdout.write(json.dumps({"v": 1, "ok": False, "error": f"{barrier.MESSAGE}."}) + "\n")
        return barrier.BUSY_EXIT_CODE
    from probe.cli import desktop, write_gate
    from probe.core import events
    from probe.sdk import agent_session

    agent_session.forgo_harness_process_session()
    refused = _desktop_refusal()
    if refused:
        from probe.sdk.redaction import scrub_string

        print(refused, file=sys.stderr)
        sys.stdout.write(json.dumps({"v": 1, "ok": False, "error": scrub_string(refused)[:1500]}) + "\n")
        return write_gate.EXIT_REFUSED
    raw = getattr(source, "buffer", None) if source is not None else None
    data = b"" if source is None else (raw.read(desktop.MAX_INPUT + 1) if raw is not None else source.read())
    if isinstance(data, str):
        data = data.encode("utf-8")
    with events.redirect_stdout() as out:
        text, code = desktop.respond(data)
        out.write(text + "\n")
    return code


def _cli_latest(*, fetch: bool) -> tuple[str | None, bool | None]:
    """The newest CLI the release manifest names, or None when unknown, and
    whether the manifest's server answered at all (None: not asked).

    Without `fetch`: the cached manifest's answer, no network (the service's
    reads after an update must stay quick). With it: the manifest itself,
    fetched with the shared TLS trust and the caller's environment (its proxy),
    and NOT written to the cache: a failed fetch here must never push the
    CLI's own refresh into its back-off (`version_policy.write_cache`). An
    error that is no network at all (a name that did not resolve, no route:
    `probe._shared.offline`) is no answer; a refused connection, a timeout,
    TLS, an HTTP error or a body that is not a manifest is one."""
    reachable = None
    try:
        from probe import version_policy

        if fetch:
            from probe.sdk.tls import ssl_context

            url, context = version_policy.base_url() + version_policy.MANIFEST_PATH, ssl_context()
            try:
                manifest = version_policy.fetch(url, context=context)
            except Exception as exc:
                # No network at all (a name that did not resolve, no route); a
                # refused connection, a timeout or TLS is an answer of a kind.
                from probe._shared import offline

                reachable = not offline.no_network(exc)
                raise
            reachable = True
        else:
            manifest, _, _ = version_policy.read_cache()
        latest = (manifest or {}).get("cli", {}).get("latest")
        return (latest if isinstance(latest, str) and latest else None), reachable
    except Exception:  # noqa: BLE001 -- unknown: the caller decides without it
        return None, reachable


def _refresh_manifest() -> dict:
    """`version {"refresh": true}`: the CLI's cached release manifest,
    refreshed as its own detached refresher does (`probe.cli.version_refresh`:
    the fetch, written to the cache with its back-off, then the update reports
    still waiting), for the Probe service's `manifest.refresh`. `{"ok",
    "fetched_at"}` from the cache it wrote. Whatever the refresher prints goes
    to stderr: stdout is this read's one object."""
    from probe.core import events

    with events.redirect_stdout():
        try:
            from probe import version_policy
            from probe.cli import version_refresh

            version_refresh.refresh_cache()
            _, fetched_at, ok = version_policy.read_cache()
        except Exception:  # noqa: BLE001 -- the service reports a failed refresh
            return {"ok": False, "fetched_at": None}
    return {"ok": bool(ok), "fetched_at": int(fetched_at) if fetched_at else None}


def _request_text(action: ActionName, source: TextIO | None) -> str:
    """The request as text: stdin's bytes as UTF-8, whatever the locale says
    (JSON is UTF-8). Bytes that are not UTF-8 are a refused request, never a
    traceback: a strict locale's `sys.stdin` would raise UnicodeDecodeError."""
    from probe.core import requests

    if source is None:
        return ""
    raw = getattr(source, "buffer", None)
    data = raw.read() if raw is not None else source.read()
    if not isinstance(data, bytes):
        return data
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise requests.RequestError(f"{action}: the request is not UTF-8 (byte {exc.start}: {exc.reason})") from None


def _dispatch(action, request) -> int:
    from probe.core import actions

    if action is ActionName.CONFIGURE:
        return actions.configure(request)
    if action is ActionName.RECORDER:
        return actions.recorder(request)
    if action is ActionName.LOGOUT:
        return actions.logout()
    if action is ActionName.UNINSTALL:
        return actions.uninstall()
    if action is ActionName.UPDATE:
        return actions.update()
    if action is ActionName.SESSION_DEFAULT:
        return actions.session_default(request)
    if action is ActionName.WORKSPACE_LIMIT:
        return actions.workspace_limit(request)
    raise AssertionError(f"no dispatch for {action}")  # every ActionName is handled above


def _usage_error(message: str) -> int:
    """A request refused before anything ran: said on stderr, and as `error` +
    `done` on stdout, as a `probe wizard --json` whose arguments do not parse."""
    from probe.core import events

    print(f"probe.core.run: {message}", file=sys.stderr)
    events.done_events(code=events.ErrorCode.USAGE, message=message.splitlines()[0], exit_code=2)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
