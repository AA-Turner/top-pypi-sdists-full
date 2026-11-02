"""The daemon's AI process: queue -> bites -> `probe` commands (daemon v2).

    probe daemon worker --session-id S --transcript T --cwd C --source claude_code

Spawned and supervised while the session's switch is `daemon`: by the Probe
service for a session it records (`probe.service.sessions.workers`), else by capture
(`tap watch`). Stopped with SIGTERM at session end -- or when it sees capture is gone
-- it reads what is on disk at that moment to its end, finishes what is queued
and exits: at most FINISH_CAP_S from that moment, a run already going included
(one still going at the deadline is cancelled, its events left queued). One per
session: it holds `<state>/probe/daemon/<sid>.lock` for its whole life, and the
worker of a resumed session waits for the previous one to finish (at most
LOCK_WAIT_S, then EXIT_RESPAWN_LATER).

    every POLL_S:  read new lines (main log, helper-agent logs, the SDK inbox)
                   -> normalized events -> scrubbed -> the store; a log
                   rewritten under its cursor is read no more (one notice)
                   answers to held questions -> run / void / refuse
                   renew the lease while recording works; leave if the switch
                   left `daemon`
    when due:      folder check (at most every FOLDER_CHECK_S, off the loop),
                   then one bite with the tools. PROBE_DAEMON_MODE picks what a
                   bite is (T15):
                     bites         a fresh model call built from disk
                                   (`bite.build`), capped per bite
                     conversation  the next run of the session's ONE
                                   conversation: a user message with the new
                                   events (`bite.build_next`) appended to the
                                   saved history, compacted near its context
                                   budget, saved after every run and resumed
                                   on respawn. A run pauses after
                                   ROUNDS_BEFORE_YIELD model rounds (below);
                                   no cap on its total work. It starts fresh
                                   from disk (a
                                   bite) when there is no usable saved history,
                                   after COMPACTIONS_BEFORE_FRESH compactions,
                                   when the loop detector stopped a run, when
                                   the model thought until its token limit and
                                   answered nothing, or when the model refused
                                   the saved history (a 4xx not about the key,
                                   budget or rate)
                   No bite starts while this process may not write for a
                   reason it did not make (the switch unreadable -- for
                   SWITCH_UNREADABLE_EXIT_S and it exits --, another process's
                   live lease)
    between two model rounds of a run (A1):
                   new lines read into the queue, answers settled, and the run
                   stopped for the switch leaving `daemon`, a lost lease, the
                   session-end deadline, or the loop detector
                   (the same failing call 3x, a refusal that reads alike in 3
                   model rounds, the same successful call 5x). A conversation run is paused after ROUNDS_BEFORE_YIELD
                   rounds: its history is saved (its last tool results
                   included), its events covered, and the next bite carries
                   on in the same conversation with what arrived meanwhile --
                   at once, even when nothing did. Every model round is
                   recorded as it arrives (T10): the
                   store's `rounds` and the device's token counter. There is no
                   spend limit (F2) and no device fuse (Richard 2026-09-28: "we
                   dont want any limit")
    when failing:  retried with growing waits (capped); after 3 failures its
                   items wait at the back while later ones go first; never
                   dropped. A refused key (by the model or by Probe on a
                   `probe` command), the budget or the model's
                   gateway failing twice in a row RELEASES the lease with its
                   reason, and it stays released until a model round answers
                   again (a key Probe refused: until Probe takes it again, and
                   no model call before). A bite its limits (bites mode), the
                   loop detector or a model that answered nothing before its
                   token limit cut short is retried over half its new events;
                   cut short twice from the same event, that range is skipped,
                   and a notice and the logbook say so
    when crashing: logged, the lease released (`error`), exit EXIT_CRASHED: the
                   supervisor waits before it starts another -- unless the CLI
                   was reinstalled under it (`install_replaced`): exit 0, and
                   the supervisor starts the new install at once

A bite is due when the queue holds a request from the main agent (`probe ask
--writer`, at any place in the queue: `requests.py`), a run start or end (at
any place, at most one run per RUN_EVENT_MIN_GAP_S), your prompt, the agent's
turn end, more than QUEUE_LIMIT_CHARS, anything older than DUE_AFTER_S (from
when it was noticed), or anything at all once the session is ending.
"""

from __future__ import annotations
import asyncio
import os
import time
from typing import Callable

from probe.shared.harness import lookup as adapters
from probe.shared.mailbox import approvals as appr
from probe.daemon.agent.model import model as model_mod
from probe.shared.harness.session_log import Adapter
from probe.shared.harness import session_filter as exclusions_mod
from probe.daemon.trace import trace as trace_mod
from probe.daemon.store.store import (
    Store,
    store_path)
from ...foundation.compose.compose import compose
from probe.daemon.worker.bite.run import BiteRunMixin, PUSHED_SETTINGS
from probe.daemon.worker.lease_keeping import LeaseMixin
from probe.daemon.worker.loop.failures import FailuresMixin
from probe.daemon.worker.loop.held import HeldAnswersMixin
from probe.daemon.worker.loop.inbox import InboxMixin
from probe.daemon.worker.loop.loop import TickMixin
from probe.daemon.worker.loop.modes.bites import BitesMixin
from probe.daemon.worker.loop.modes.conversation import ConversationMixin, _compaction_available
from probe.daemon.worker.loop.reading import CATCH_UP_PENDING, ReadingMixin
from probe.daemon.worker.loop.requests import RequestsMixin
from probe.daemon.worker.loop.run_end import RunEndMixin
from probe.daemon.worker.loop.stretches import READ_ONLY_FROM, READ_ONLY_TURN, StretchesMixin
from probe.daemon.worker.loop.triggers import TriggersMixin


@compose
class Worker(
    LeaseMixin,
    ReadingMixin,
    InboxMixin,
    RequestsMixin,
    TriggersMixin,
    BiteRunMixin,
    BitesMixin,
    ConversationMixin,
    RunEndMixin,
    FailuresMixin,
    HeldAnswersMixin,
    TickMixin,
    StretchesMixin,
):
    def __init__(self, session: Session, *, clock=time.time, replay=None, model=None) -> None:
        self.session = session
        self.clock = clock
        self.adapter: Adapter = adapters.for_source(session.source)
        self.store = Store(store_path(session.session_id), clock=clock)
        #: Per chat stream: did its last read stop at READ_CHUNK_BYTES with whole
        #: lines still waiting (a backlog read a chunk a poll)?
        self.stream_behind: dict[str, bool] = {}
        if replay is None and self.store.next_seq() == 1 and self.store.cursor("main")[0] is None:
            # The session's first worker: what the session already holds is read
            # before any bite or reader turn, then judged once (`_catch_up`).
            with self.store.tx():
                self.store.set_fact(CATCH_UP_PENDING, True)
        self._catch_up_pending = bool(self.store.fact(CATCH_UP_PENDING))
        #: The newest stamp of any main chat line this worker has read (`_parse`).
        self.chat_seen_at: float | None = None
        self._start_reader_log()
        #: The writer's trace in the session's folder (`trace.py`): each bite's
        #: start and end from here, its model calls and tool runs from the agent.
        self.trace = trace_mod.TraceFile(session.session_id, "writer")
        self.store.on_bite_closed = lambda row: self.trace.end_run(row.pop("bite"), **row)
        self.board = appr.Board(clock=clock)
        self.replay = replay
        self._model = model
        self.stopping = False
        self.finish_by: float | None = None
        #: Where each stream ended when stopping began (`begin_stopping`), and
        #: whether it was read to there yet (`_take_input`).
        self._stop_ends: dict[str, int] | None = None
        self.drained = False
        self.failures = 0
        #: Bites in a row whose model answered nothing (NO_ANSWERS_BEFORE_RELEASE).
        self.no_answers = 0
        self.next_attempt_at = 0.0
        #: When the last run started (`clock`): the writer's least gap counts from it.
        self.last_run_at = float("-inf")
        model_mod.restore_pushed(self.store.fact(PUSHED_SETTINGS))
        #: Why the next run starts a fresh conversation, for its trace (`fresh`): "cold"
        #: when an idle conversation was ended (F2); None otherwise.
        self._fresh_why: str | None = None
        #: When the last run a request started began (REQUEST_RUN_MIN_GAP_S counts from it).
        self.last_request_run_at = float("-inf")
        #: Why this worker released the lease; renewing waits until a model round answers again.
        self.released_reason: str | None = None
        #: The last release had no network at all (`probe.foundation.tls.network_down`).
        self.released_offline = False
        self.parent_pid = os.getppid()
        #: In the daemon host: has this run's owner gone (its connection closed)?
        #: None per process, where the parent and the supervisor's identity tell.
        self.supervisor_gone: Callable[[], bool] | None = None
        #: In the daemon host: called once per poll (its heartbeat). None per process.
        self.on_tick: Callable[[], None] | None = None
        #: In the daemon host: an idle run waits for a poke (`pause`). False per process.
        self.wakeable = False
        #: The session's running worker (`run_session`): its marker says it takes
        #: requests, and every poll writes it again when it is gone (`_keep_mailbox`).
        self.marks_requests = False
        #: When this run last saw something new (`clock`): idle after IDLE_AFTER_S.
        self.changed_at = clock()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._wake: asyncio.Event | None = None
        self._reader_wake: asyncio.Event | None = None
        #: The supervisor's identity (SUPERVISOR_PID_ENV), when it gave one.
        self.supervisor: tuple[int, str | None] | None = None
        self.folders_checked_at = float("-inf")
        self.settle_retry: dict[str, tuple[int, float]] = {}  # request id -> (failures, next try)
        #: Bites in a row whose model gateway failed (L-1); a model round answering resets it.
        self.gateway_failures = 0
        #: Since when the session's switch cannot be read (None: it can).
        self.switch_unreadable_since: float | None = None
        #: Why the last due bite did not start (logged once per reason).
        self.not_started: str | None = None
        #: Probe itself (not the model) refused the key: a model round answering does
        #: not take the lease back until a Probe auth check passes (`_probe_accepts_key`).
        self.probe_refused_key = False
        #: The reader (daemon reads), started in `loop` when reads are on.
        self.reader = None
        #: The run-alert poller (`run_alerts.py`), started with the reader: the
        #: same mailbox, the same switch.
        self.run_alerts = None
        #: The team-note audit (daemon-team-note-audit), made in `loop`; it starts
        #: itself at most once per session, on the researcher's first prompt.
        self.audit = None
        #: `/probe inline`: the intervals the last marking pass saw, and the
        #: highest event seq it examined (only newer events are checked until the
        #: intervals change).
        self._inline_seen: tuple = ()
        self._inline_seq = 0
        #: While the switch reads `read only (daemon)`: the first event seq, and the
        #: turn, it began at. Events from there are the reader's alone (never
        #: recorded). Kept in the store, so a worker started after a crash knows.
        started = self.store.fact(READ_ONLY_FROM)
        self.read_only_from: int | None = int(started) if started is not None else None
        self.read_only_turn = int(self.store.fact(READ_ONLY_TURN) or 0)
        self.mode = daemon_mode()
        #: The writer's event indexer (`WriterEvents.INDEX`), built on its first use.
        self._index_model = None
        if self.mode == Mode.CONVERSATION and not _compaction_available():
            self.mode = Mode.BITES
        if self.mode == Mode.BITES:
            self._end_conversation_for_bites()
        self.store.set_fact("harness", self.adapter.name)
        self.store.set_fact("cwd", str(session.cwd))
        self.exclusions = exclusions_mod.Filter(self.store, session.session_id, session.cwd)
        self._interrupted_yeses()
from probe.daemon.worker.env import Session  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.mode import Mode, daemon_mode  # noqa: E402 -- pieces need each other; the front door loads this one first
