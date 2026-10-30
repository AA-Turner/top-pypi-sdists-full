"""The `probe` reads the daemon answers inside the daemon host, never as a new
process (R38, Richard 2026-10-29: "daemon reads shouldn't ever be starting a new
process per call, it should be using the probe service").

`tools.run_probe_process` is every `probe` command's one door (plain code's own
reads for the writer, its message's runs, come in by `tools.read_in_host`: here
or not at all). A read in MOVED
is answered here, by the CLI command's own body (`probe.cli.reads`), in the host
the Probe service already runs: no process, no interpreter start, no CLI import,
an HTTP call or two. Everything else -- a write, a read not moved yet, a help
request, a root option, words click refuses (the CLI words the refusal), an
option that runs something on this machine (LOCAL_SIDE_EFFECTS) -- still runs as
the CLI in a process of its own, and a read among those is counted
(`tools.PROBE_READS_FACT`, a log line naming it) so the remainder stays visible.
So does a moved read the host hands back (`start`/`answer` answer None): a full
in-flight slot, an outbox too large to parse here, a bug in the body.

    MOVED     86% of the 3,724 reads the daemons on one box spawned (10-28/29):
              run get 781, run check 581, notes find 498, outbox status 445,
              run reproduce 441, project get 280, experiment get 185

THE SESSION'S PROBE, AS ARGUMENTS. One host runs every recorded session's
worker, ~40 at once. A read is answered with ITS session's key, URL and session
id, passed in: the environment its spawned CLI would have had (`env`, built by
`tools.run_probe_process`: `_base_env()` and the session's `probe_env`),
`Settings` resolved from that mapping (`config.resolve(env=)`), a client built
from them, and the mapping itself for `outbox status`. The agent session and
the time of the work its requests name are that environment's too
(`queued_session_scope`, `event_at_scope`), never the process's (in the host,
`os.environ` is the coding agent's own). Nothing is kept between calls but
two bounds: the in-flight slots of each run and one outbox parse at a time.

What the spawned CLI did besides its command is not done here: its root
callback (the outbox banner and its kicks, the update and repair notices) and
the SDK's process-level warnings, which go to the host's log. The CLI's own
transport settings outside `env` (a proxy, a certificate bundle) are the
session's environment, as for the daemon's other reads (`probe_api`).

TIMEOUT AND CANCELLATION: a thread with a deadline. The SDK client is
synchronous and the CLI's own body is what runs (one body, one output), so a
read runs on a thread of its own, as the session's run (`runctx`: its logs, its
state), inside `transport.deadline_scope`: no request starts, and none reads on,
past the command's budget plus THREAD_GRACE_S. The caller (`tools._in_host`)
stops waiting at once on its own deadline, on lease loss and on cancellation,
with the words the spawned CLI's stop used; the thread -- a read, with nothing
to undo -- ends by its deadline on its own (its local file reads are bounded:
OUTBOX_HOST_OPS).
"""

from __future__ import annotations

import asyncio
import contextvars
import functools
import io
import logging
import os
import threading
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from probe.daemon import precheck, runctx

log = logging.getLogger("probe.daemon.tools")

#: The reads answered in the host (see the module's docstring).
MOVED = frozenset({"run get", "run check", "notes find", "outbox status", "run reproduce", "project get",
                   "experiment get"})
#: A moved read's option that runs something on this machine keeps it the CLI's:
#: `run check --verify` fetches the run's code commit with git
#: (`snapshot.commit_on_remote`), which in the host would run with the coding
#: agent's whole environment and a cache every session shares.
LOCAL_SIDE_EFFECTS = frozenset({("run check", "verify")})
#: The most in-host reads one run has in flight; past it a read runs as the CLI
#: (a read its caller stopped waiting for keeps its slot until it ends).
IN_FLIGHT_PER_RUN = 8
#: An `outbox status` over more queued ops than this runs as the CLI: it parses
#: every op file (a queue holds up to 500,000), local work no deadline stops,
#: which in the host would hold every session's loop and stay in its memory.
OUTBOX_HOST_OPS = 2_000
#: A read's own deadline is this much later than its caller's: the caller's stop
#: ("stopped after Ns") is what the model reads, never the thread's.
THREAD_GRACE_S = 1.0

#: Each run's in-flight slots (`runctx.Shared`; outside a run, this process's).
_IN_FLIGHT = threading.BoundedSemaphore(IN_FLIGHT_PER_RUN)
_in_flight = runctx.Shared(globals(), "_IN_FLIGHT", lambda: threading.BoundedSemaphore(IN_FLIGHT_PER_RUN))
#: One in-host outbox parse at a time, host-wide: a large one never piles up.
_OUTBOX_PARSE = threading.Lock()


@dataclass(frozen=True)
class Call:
    """A moved read, parsed as the CLI parses it to run it."""

    path: str
    params: dict
    #: The command's click context (`precheck.command_context`): a usage error
    #: the body raises (an unknown ref, a bad --fields) is worded against it.
    ctx: Any


@dataclass(frozen=True)
class Route:
    """Where `probe <argv>` runs: `call` when the host answers it; else the CLI,
    and `read` names the command when it is a read (counted as spawned)."""

    call: Call | None = None
    read: str | None = None


def route(argv: list[str]) -> Route:
    try:
        parsed = precheck.parse(argv)
    except precheck.ParseError:
        return Route()
    if parsed.owner != precheck.READ:
        return Route()
    local = any(parsed.params.get(option) for path, option in LOCAL_SIDE_EFFECTS if path == parsed.path)
    if parsed.path in MOVED and not parsed.help and not parsed.root_options and not local:
        ctx = precheck.command_context(argv)
        if ctx is not None:
            return Route(call=Call(parsed.path, dict(ctx.params), ctx))
    return Route(read=parsed.path)


class _Declined(Exception):
    """The host leaves this read to the CLI."""


def _client(settings: Any, env: Mapping[str, str]) -> Any:
    """The client a read uses: the session's settings, the CLI's surface and
    version, synchronous, its outbox where that CLI's would be (it queues
    nothing: these only read)."""
    from probe import __version__
    from probe.client_headers import client_version_headers
    from probe.sdk.client import Client
    from probe.sdk.journal import default_dir
    from probe.sdk.surface import Surface

    client = Client(settings=settings, spool_dir=default_dir(env), surface=Surface.CLI.value,
                    client_headers=client_version_headers("cli", __version__), async_writes=False,
                    attribution="ambient")
    # As the CLI's (`main._new_client`): a refusal fails, never prints `null`.
    client.raise_permanent = True
    return client


def _queued_more_than(journal: Any, limit: int) -> bool:
    """Does `journal` (its own queue and its credential queues) hold more than
    `limit` op files? Counted by name, never read, stopping past `limit`."""
    seen = 0
    for queue in journal.namespaces():
        for folder in (queue.ops_dir, queue.failed_dir):
            try:
                with os.scandir(folder) as entries:
                    for _ in entries:
                        seen += 1
                        if seen > limit:
                            return True
            except OSError:
                continue
    return False


def _outbox_status(api: Any, env: Mapping[str, str], params: dict, deadline: float) -> Any:
    """`probe outbox status` over the session's CLI's outbox and every other one
    of this user here (`main._outbox_journals`, from `env`); the CLI's when the
    outbox is too large to parse here (OUTBOX_HOST_OPS)."""
    from probe.cli import reads
    from probe.sdk.journal import Journal, default_dir

    current = Journal(default_dir(env))
    if _queued_more_than(current, OUTBOX_HOST_OPS):
        raise _Declined
    if not _OUTBOX_PARSE.acquire(timeout=max(0.0, deadline - time.monotonic())):
        raise _Declined  # the caller stopped waiting already
    try:
        others = [Journal(d) for d in Journal.discover(env) if d != current.dir]
        return reads.outbox_status(api, current, others, params["verbose"], params["run"])
    finally:
        _OUTBOX_PARSE.release()


#: Each moved read's body, from its parsed parameters.
_BODIES: dict[str, Callable[[Any, dict], Any]] = {
    "run get": lambda api, p: _reads().run_get(api, p["run"], p["fields"]),
    "run check": lambda api, p: _reads().run_check(api, p["run"], p["verify"]),
    "notes find": lambda api, p: _reads().notes_find(api, list(p["words"]), project=p["project"],
                                                     experiment=p["experiment"], run=p["run"], note=p["note"]),
    "run reproduce": lambda api, p: _reads().run_reproduce(api, p["run"]),
    "project get": lambda api, p: _reads().project_get(api, p["project_id"], p["fields"]),
    "experiment get": lambda api, p: _reads().experiment_get(api, p["experiment_id"]),
}


def _reads():
    from probe.cli import reads

    return reads


def answer(call: Call, env: Mapping[str, str], deadline: float) -> tuple[int | None, str, str] | None:
    """`(exit code, stdout, stderr)` of `call`, as the CLI run with `env` would
    print them; every request made by `deadline` (`time.monotonic()`). None:
    the CLI answers it (`_Declined`, or a bug here). Runs on the read's own
    thread (`start`)."""
    from probe.cli import reads
    from probe.sdk import agent_session, config
    from probe.sdk.transport import deadline_scope, event_at_scope, queued_session_scope

    resolve = functools.partial(config.resolve, env=env)
    try:
        with deadline_scope(deadline), queued_session_scope(agent_session.queued_session(env)), \
                event_at_scope(agent_session.queued_event_at(env)):
            if call.path == "outbox status":
                printed = _outbox_status(reads.Api(client=None, resolve=resolve, env=env), env, call.params,
                                         deadline)
            else:
                with _client(resolve(), env) as client:
                    printed = _BODIES[call.path](reads.Api(client=client, resolve=resolve, env=env), call.params)
    except _Declined:
        return None
    except Exception as exc:  # noqa: BLE001 -- reported as the CLI reports it, or left to the CLI
        return _failed(call, env, exc)
    return printed.code, printed.out, printed.err


def _usage_width(ctx: Any, env: Mapping[str, str]) -> None:
    """A usage error wraps where the spawned CLI's did: click's help width from
    that CLI's COLUMNS, never the process's."""
    try:
        columns = int(env.get("COLUMNS") or 80)
    except ValueError:
        columns = 80
    ctx.terminal_width = max(min(columns, ctx.max_content_width or 80) - 2, 50)


def _failed(call: Call, env: Mapping[str, str], exc: Exception) -> tuple[int | None, str, str] | None:
    """What the CLI's `main` prints for `exc` (`reads.report_error`); a usage
    error is worded against the command's own context, as click's invoke does.
    None for anything else -- a bug in this path, or code changed under the host
    by an update -- and the CLI answers instead."""
    import typer

    from probe.cli import reads
    from probe.sdk.agent_session import DAEMON_SESSION_ENV

    if isinstance(exc, typer.Exit):
        return int(exc.exit_code), "", ""
    if isinstance(exc, typer.Abort):
        return 1, "", "aborted\n"
    if isinstance(exc, reads.ClickException) and getattr(exc, "ctx", None) is None:
        _usage_width(call.ctx, env)
        exc.ctx = call.ctx
    said = io.StringIO()
    code = reads.report_error(exc, said, daemon_session=bool(env.get(DAEMON_SESSION_ENV)))
    if code is None:
        log.error("probe %s raised in the daemon host; the CLI answers it instead", call.path, exc_info=exc)
        return None
    return code, "", said.getvalue()


def start(call: Call, env: Mapping[str, str], timeout: float) -> asyncio.Future | None:
    """Run `call` on a thread of its own, as this run, by `timeout` (plus
    THREAD_GRACE_S) seconds from now; the returned future (of the running loop)
    gets its `(code, stdout, stderr)`, or None when the CLI answers it. None at
    once when this run has IN_FLIGHT_PER_RUN reads in flight. Nobody need wait
    for the future: a read stopped waiting for ends by its deadline, its answer
    dropped."""
    slots = _in_flight.get()
    if not slots.acquire(blocking=False):
        return None
    loop = asyncio.get_running_loop()
    done: asyncio.Future = loop.create_future()
    context = contextvars.copy_context()  # the session's run: its logs, its state
    deadline = time.monotonic() + timeout + THREAD_GRACE_S

    def settle(result: tuple[int | None, str, str] | None) -> None:
        if not done.done():
            done.set_result(result)

    def work() -> None:
        try:
            result = context.run(answer, call, env, deadline)
        except BaseException:  # noqa: BLE001 -- never a thread dying unheard: the CLI answers it
            log.error("probe %s died in the daemon host; the CLI answers it instead", call.path, exc_info=True)
            result = None
        finally:
            slots.release()
        try:
            loop.call_soon_threadsafe(settle, result)
        except RuntimeError:
            pass  # the run's loop is gone: nobody waits for this read now

    run = runctx.current()
    who = f"run-{run.session_id[:12]} " if run is not None else ""
    threading.Thread(target=work, name=f"{who}probe-read {call.path}", daemon=True).start()
    return done
