"""Hints: the team's nearest records, shown to a coding agent (Probe hints T3).

When a session's researcher prompt, a peer agent's message, a web search or a
Probe run launch looks near the team's work, the agent is shown the few team
records nearest to it at its next prompt or tool call. The lookup runs here,
once per machine, and never blocks anything:

    the feed      every session a recorder of this service holds now
                  (`recorders.py`; its claim held, so not while capture is off,
                  the folder is disabled or another recorder has it), registered
                  live and unconfined, not `off`. Its recorder is the tap's loop
                  (`tap.hosted`), which reads the transcript into the journal and
                  hands no line out, so this lane keeps its own offset in the
                  same file: one look every POLL_S per session (an open and an
                  fstat), and only the new bytes read (the page cache has them: the recorder just read
                  them). New whole lines are parsed with the daemon's adapter
                  (`probe.shared.harness.lookup`, the worker's parse) and its
                  `.probe.config` filter (`exclusions.Filter`, the worker's), so
                  the events are the daemon's. A session first seen starts near
                  its end: only lines younger than FRESH_S there count
    triggers      a researcher prompt (`prompt`); a peer agent's message (META,
                  tool `events.PEER_TOOL`, `peer`; its sender's session excluded,
                  found from its socket in Claude Code's `sessions/<pid>.json`:
                  the sender's own transcript holds the message it sent); a
                  WebSearch / WebFetch call (`search`); a shell call that starts
                  a Probe run for certain: `probe exec` opening a new run, or
                  `probe run start` (`command`); and (`window`, plan
                  hints-window-trigger W1) WINDOW_GAP_S after the last window
                  look, the researcher's prompt or the turn's first step (a
                  turn's end ends its window), at the agent's next step, when it
                  wrote at least one message since: every such message, newest
                  first, each looked up on its own (`segments`). Tool calls and
                  their output are never sent for a window. Nothing else
    the lookup    POST /v1/hints on one kept connection per lookup thread
                  (prompts and the rest on one, windows on their own), with the read-only key
                  of the session's CLI config (KEYS), TIMEOUT_S, failing open:
                  no answer is no hint. The text goes through the capture's
                  secret scan first (`scrubbed`), as all transcript text that
                  leaves the machine does
    limits        one request per session per SESSION_GAP_S, windows and the
                  rest each on their own clock: a window just sent never delays
                  the session's prompt (a newer trigger
                  replaces the one waiting, but a search or a command never a
                  prompt or a peer's message); a token bucket for the machine
                  (BUCKET_PER_MIN, BUCKET_BURST); holds as `alertpoll` keeps
                  them (`_scopes`): a 429 holds that key on that server
                  LIMITED_S, a 401 / 403 the key REFUSED_S, a 404 the server
                  MISSING_S; `mode: off` quiets that key on that server
                  OFF_RECHECK_S for every session; the last REPEATS texts of a
                  session are never sent again. A window lookup goes on its
                  own thread, so it never holds up a prompt's; it never takes
                  the machine's last tokens (WINDOW_TOKEN_RESERVE), waits
                  WINDOW_TIMEOUT_S, and
                  is held on its own (`_window_scopes`): a 404, or a 422 naming
                  `trigger`, holds window lookups on that server MISSING_S, no
                  answer LIMITED_S, a 429 that key's there LIMITED_S; prompts
                  and the rest still ask
    delivery      `fire` with a `hint` (as Probe rendered it, at most
                  MAX_HINT_CHARS: a longer one is dropped whole): an unasked
                  message with origin
                  `mailbox.ORIGIN_HINT` (a slot of its own beside the reader's),
                  posted in this process with the mailbox
                  service's own step (`MailHost.post`); the reads hook hands it
                  over at the agent's next prompt or tool call (daemon and inline
                  sessions: both plugins run it). Never when every record in it
                  was delivered to the session already (the claim log, and a
                  ledger of which records each hint carried) or is waiting in
                  one; a record whose date changed counts as new. Those records'
                  doc ids go with each request (`exclude_doc_ids`) for the
                  server to leave out. A newer researcher prompt, or the end of
                  the agent's turn, withdraws a hint still waiting
    markers       `<sid>.live` (`mailbox.hints_live_path`) while the lane can
                  hint the session: its daemon's reader then leaves prompt time
                  to hints. `<sid>.window` (`mailbox.hints_window_path`) only
                  while window hints are proven working for it (`_window_works`):
                  its daemon's reader then stops its check-ins
    off           PROBE_HINTS=off in a session's environment (its recorder's
                  `env`: every PROBE_* variable the agent's shell had), or in
                  the service's own

One log line per lookup (trigger, mode, fire, reason, top score, latency,
how long after the trigger it was answered, delivered or why not), never the
text. Three daemon threads of its own (the tail, the lookups, the window
lookups), none waited for at exit; all idle without a timer while no session is
followed; everything they do is caught and logged.

Stdlib only at import (the service's start path); the daemon's adapters, its
filter and the mailbox are imported on the lane's threads.
"""

from __future__ import annotations

import contextlib
import os
import threading
import time
from collections import Counter, OrderedDict
from collections.abc import Callable
from pathlib import Path

from ..watch.alertpoll import Endpoint
from ...foundation.compose.compose import compose
from probe.service.hints.delivery import delivered_ids, post_message, waiting_hints, withdraw_hints
from probe.service.hints.ledger import LedgerMixin
from probe.service.hints.lookups import LookupsMixin
from probe.service.hints.request import HintFetcher, credentials
from probe.service.hints.state import BUCKET_BURST, Lookup, _State, disabled
from probe.service.hints.tail import TailMixin, _Tail
from probe.service.hints.triggers.peer import Senders
#: Every followed transcript is looked at this often: one stat each, and only
#: new bytes read. A prompt waits half of it on average before its lookup goes
#: (1.0 s until plan hints-latency L3: ~0.5 s of a ~1.5 s hint).
POLL_S = 0.25
#: Test-only: a shorter POLL_S (nothing in production sets it).
POLL_ENV = "PROBE_SERVICE_HINTS_POLL_S"


def _poll_interval() -> float:
    try:
        value = float(os.environ.get(POLL_ENV) or POLL_S)
    except ValueError:
        return POLL_S
    return value if value > 0 else POLL_S


@compose
class HintLane(
    TailMixin,
    LookupsMixin,
    LedgerMixin,
):
    """The service's one hint lane (see the module docstring).

    `sessions()` lists the sessions to read (`followed`), asked on the lane's
    tail thread. Seams for tests: `transport(endpoint, body) -> (status, data)`,
    `endpoint_of(env)`, `post(sid, state, message) -> bool`, `withdraw(sid,
    state) -> [ids]`, `delivered(sid, state) -> {ids}`, `waiting(sid, state) ->
    {ids}`, `senders` (where Claude Code's session records are), the clocks.
    `posted(sid)` is told of each hint posted (the server says
    `mailbox.changed`)."""

    def __init__(
        self,
        *,
        sessions: Callable[[], list],
        log: Callable[[str], None],
        version: str = "0.0.0",
        environ: dict | None = None,
        transport: Callable | None = None,
        endpoint_of: Callable[[dict], Endpoint | None] = credentials,
        post: Callable[[str, str, dict], bool] = post_message,
        withdraw: Callable[[str, str], list] = withdraw_hints,
        delivered: Callable[[str, str], set] = delivered_ids,
        waiting: Callable[[str, str], set] = waiting_hints,
        posted: Callable[[str], None] = lambda sid: None,
        senders: Senders | None = None,
        ledger_dir: Path | None = None,
        clock: Callable[[], float] = time.monotonic,
        wall: Callable[[], float] = time.time,
        poll_s: float | None = None,
    ) -> None:
        self._sessions = sessions
        self._log = log
        self.version = version
        self.enabled = not disabled(os.environ if environ is None else environ)
        self.transport = transport if transport is not None else HintFetcher(version)
        #: The window thread's own: a fetcher's kept connections are not shared
        #: across threads. A test's `transport` serves both.
        self.window_transport = transport if transport is not None else HintFetcher(version)
        self.endpoint_of = endpoint_of
        self._post = post
        self._withdraw = withdraw
        self._delivered = delivered
        self._waiting = waiting
        self._posted = posted
        self.senders = senders if senders is not None else Senders()
        self._ledger_dir = ledger_dir
        self.clock = clock
        self.wall = wall
        self.poll_s = _poll_interval() if poll_s is None else poll_s
        self._tails: dict[str, _Tail] = {}
        self._states: dict[str, _State] = {}
        self._pending: OrderedDict[str, Lookup] = OrderedDict()
        self._cv = threading.Condition()
        self._tokens = BUCKET_BURST
        self._filled_at = clock()
        #: Requests wait until then (`clock`) per scope (`_scopes`): a refused key,
        #: a server without the route, a 429 for a key on a server.
        self._holds: dict[tuple, float] = {}
        #: `mode: off`: (base URL, key) -> until when it is not asked again.
        self._off: dict[tuple, float] = {}
        self._wake = threading.Event()
        self._threads: list[threading.Thread] = []
        self._closed = False
        #: When the ledgers were last swept (`clock`), or None before the first.
        self._swept_at: float | None = None
        #: What happened, counted (tests and the log): triggers, skips, posts.
        self.stats: Counter = Counter()
        #: When each served session's hint marker was last touched (`clock`).
        self._beats: dict[str, float] = {}
        #: (base URL, key) whose window lookups the server answered as such (a 200
        #: with `trigger_class: window`), with no 404 / 422 naming `trigger` since (W3).
        self._window_ok: dict[tuple, bool] = {}
        #: (base URL, key) -> its window lookups failed in a row, whichever session's.
        self._window_key_failures: dict[tuple, int] = {}

    # -- lifecycle --------------------------------------------------------------

    def changed(self) -> None:
        """A recording started or changed: look now (the threads start on the first)."""
        if not self.enabled or self._closed:
            return
        try:
            if not self._threads:
                for name, target, args in (("hints-tail", self._tail_loop, ()),
                                           ("hints-lookup", self._lookup_loop, (False,)),
                                           ("hints-window", self._lookup_loop, (True,))):
                    thread = threading.Thread(target=target, args=args, name=name, daemon=True)
                    self._threads.append(thread)
                    thread.start()
            self._wake.set()
        except Exception as exc:  # noqa: BLE001 -- no hints, nothing else touched
            self._log(f"hints: could not start: {exc!r}")

    def close(self) -> None:
        self._closed = True
        self._wake.set()
        with self._cv:
            self._cv.notify_all()
        for transport in {id(t): t for t in (self.transport, self.window_transport)}.values():
            abort = getattr(transport, "abort", None)
            if abort is not None:
                with contextlib.suppress(Exception):
                    abort()

    def _state(self, sid: str) -> _State:
        state = self._states.get(sid)
        if state is None:
            state = self._states.setdefault(sid, _State())  # both threads ask: one wins
        return state
