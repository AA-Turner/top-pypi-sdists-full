"""`python -m probe.core.run <action>`: one Probe action, as a child process.

The Probe service runs every action this way (plan R9: the event stream owns
the process's stdout, which a server cannot give one request), and the
desktop app can too. The contract is `probe wizard --json`'s:

    argv    one action: configure | recorder | logout | uninstall | update |
            session_default | status | version. Spawn it as `<python> -I -m
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
            `version` writes `{"cli_version": "<the installed CLI's>"}`.
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
        request = requests.parse_json(action, _request_text(action, sys.stdin if stdin is None else stdin))
    except requests.RequestError as exc:
        return _usage_error(str(exc))

    if action is requests.ActionName.VERSION:
        # What this process imported: after `uv tool upgrade`, the new files.
        import json

        from probe import __version__

        sys.stdout.write(json.dumps({"cli_version": __version__}) + "\n")
        return 0

    from probe.sdk import agent_session

    try:
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
