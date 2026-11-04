"""
Direct-connect transport: control plane (gateway) + data plane (worker), kept apart.

── Why this file exists ───────────────────────────────────────────────
`connect(model)` used to point one kept-alive `httpx.Client` at the gateway and send every
`/v1/act` through it. That put a gateway hop on the hot path of a control loop — the exact cost
the SDK's single reused connection exists to remove
. Direct-connect splits the two planes:

    control plane   gateway   POST /v1/act/connect   admission/quota, ensure the worker is up,
                                                     hand back worker coords + a pinned cert
                                                     fingerprint (or, `tls: "public"`, the name its
                                                     certificate is issued for) + a per-worker
                                                     secret + a lease
    data plane      worker    POST {worker_url}/act  every steady-state act, direct, reusing one
                                                     checked TLS connection, Bearer <direct_secret>

The gateway is off the hot path: after one connect, N acts ride one worker TLS connection and
the gateway observes none of them. Recovery (401 / worker-gone / lease expiry / warming) folds
back through the gateway transparently, so the caller's loop never has to reconnect by hand.

`DirectConnection` presents the same `post`/`get`/`close` surface `Policy` already drove a
`Transport` through, so the whole control loop in `act/policy.py` is unchanged: `_request`
still does `self._t.post("/v1/act", payload)`, and this class routes that one path to the
worker while `/v1/models` and `/v1/act/ready` stay on the gateway.

The data plane is worker_transport.py's (one kept-alive client to one worker's `/act`), the pin
pinned_tls.py's (the worker's certificate checked by the fingerprint the gateway pinned). A robot's observations between
acts are direct_observe.py's, its episodes direct_episode.py's: DirectConnection mixes both in.

Stdlib `ssl` + `hashlib` only for the pin (no `cryptography`, no `certifi`); httpx-only, Python 3.9-clean (no runtime `X | Y`, no `match`); and none
of the three imports `sequence_base`.
"""

from __future__ import annotations

import concurrent.futures
import copy
import logging
import random
import sys
import threading
import time
import uuid
import weakref
from datetime import datetime, timezone
from typing import Any, Callable, NamedTuple, Optional

from ..errors import AuthError, Conflict, InternalError, InvalidRequest, SequencesError, Unavailable
from . import act_size
from .transport import DEFAULT_TIMEOUT_S, Transport
from .warn import warn
from .connect_trace import ConnectTrace
from .reporting import error_of
from . import marked_observe as _marked
from . import observe_stream as _observe
from .worker_transport import _RESENDS, _STILL_OPENING, _WorkerGone, _WorkerTransport, _wait_set
from .direct_episode import _EPISODE_LOST, _STATE_GONE, _Episodes



_NO_PLACE = "no_place"



_COPY_STUCK = "copy_stuck"
from .direct_observe import _ObservationStream
from . import seat as _seat



_log = logging.getLogger(__name__)







_ANSWER_MARGIN_S = 10.0


class NotOpen(NamedTuple):
    """Why the connection to a worker was not open when DirectConnection.connect_ahead stopped waiting for it."""

    stage: str

    failed: Optional[str]

    waited_s: float


def _busy_backoff(attempt: int, retry_after_s: Optional[float]) -> float:
    """
    How long to wait before replaying an act that a busy worker (429) refused.

    Exponential from 50 ms with full jitter, capped by the worker's own Retry-After. The cap is the
    server's number; the start is not, because the worker rounds Retry-After up to a whole second (the
    header's resolution) while the slot it waits on frees after one inference — sleeping the full
    second on every collision would stall a 15 Hz loop for fifteen control periods. The jitter keeps
    robots that share a worker from replaying in lockstep and colliding again.



    """
    cap = retry_after_s if retry_after_s and retry_after_s > 0 else 1.0

    return random.uniform(0.5, 1.0) * min(cap, 0.05 * (2 ** min(attempt - 1, 10)))





_SAY_BUSY_AFTER_S = 5.0




_SAY_BY_WITHIN_S = 2 * 3600.0


_DATED_FROM_S = 24 * 3600.0


def _now() -> datetime:
    """This machine's clock, in UTC: the one every time said here is measured from."""
    return datetime.now(timezone.utc)


def _moving_words(notice: dict, *, moved: bool = False) -> str:
    """Why a robot moves to another worker, as the platform said it at a renewal (`rotate`: its reason, and by when it
    is moved whatever it is doing): its worker has served its hours - replaced by one started beside it, at a
    deployment's cap too -, a newer version serves, or its worker cannot answer it
    in time beside the robots nearer
    it - and stays, for them. The latest it is moved by only when that is near. {worker 6, cl7 dev acceptance item 12 on
    cl7a3 10-30: a far robot told over would have read "its worker is leaving"}"""
    reason = str(notice.get("reason"))

    why = {"rotate": "its worker has served its hours and is being replaced",
           "version": "the deployment now serves another version",
           "over": "its worker cannot answer it in time beside the robots nearer it",

           "more robots than seats": "its worker now seats fewer robots than it holds"}.get(reason,
                                                                                            "its worker is leaving")
    if moved:
        return why.replace("is being replaced", "was replaced") + ", and the robot had not reached an episode boundary"
    to = "to it" if reason == "version" else "to a new worker"
    by = notice.get("by")
    return (f"{why}; the robot moves {to} at an episode boundary"
            + (f", by {_clock_face(by)} at the latest" if by and _soon(by) else ""))


def _soon(stamp: Any) -> bool:
    """Whether an instant the platform said is within _SAY_BY_WITHIN_S from now (False when it does not read as one)."""
    try:
        at = datetime.fromisoformat(str(stamp).strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    at = at if at.tzinfo else at.replace(tzinfo=timezone.utc)
    return (at - _now()).total_seconds() <= _SAY_BY_WITHIN_S


def _clock_face(stamp: Any) -> str:
    """An instant the platform said (ISO; UTC when it has no offset) as this machine's clock shows it, to the minute -
    "10:12 EDT", after its date only when it is a day or more from now (_DATED_FROM_S) - rounded down, so a deadline
    said so is never later than the platform's. As said when it does not read as one."""
    try:
        at = datetime.fromisoformat(str(stamp).strip().replace("Z", "+00:00"))
    except ValueError:
        return str(stamp)
    at = at if at.tzinfo else at.replace(tzinfo=timezone.utc)
    local = at.astimezone()
    face = local.strftime("%H:%M %Z").strip()
    return face if abs((at - _now()).total_seconds()) < _DATED_FROM_S else f"{local:%Y-%m-%d} {face}"


def _ready(notice: Optional[dict]) -> bool:
    """Whether a move the robot asks for now would take it off the leaving worker, as the platform said it (`ready`)."""
    return isinstance(notice, dict) and notice["ready"] is True





_RENEW_AGAIN_S = 2.0
_RENEW_AGAIN_MAX_S = 60.0


_LEAVING_ASK_S = 30.0


_RENEW_AHEAD_BEATS = 2.5


_RENEW_AHEAD_ACTED_S = 30.0

_RENEW_AHEAD_TIMEOUT_S = 10.0





_STANDBY_PING_S = 60.0


_SWITCH_ASK_S = 0.5








_STANDBY_ASK_S = 20.0




_STANDBY_FAST_S = 240.0


class DirectConnection(_ObservationStream, _Episodes, _seat._KeptSeat):
    """
    Control/data-plane split behind the `Transport` surface `Policy` already drives.

    `post("/v1/act", ...)` goes to the worker; `get(...)` (catalogue, readiness) stays on the
    gateway. First use lazily runs one `POST /v1/act/connect`, so a warm session that never
    reconnects makes exactly one control-plane call and every act after it is direct — and a
    caller who only constructs the handle (or whose host is unreachable) pays nothing until the
    first request, exactly as the old lazy `Transport` did.
    """

    def __init__(self, gateway: Transport, model: str, *,
                 timeout_s: Optional[float] = None,
                 max_reconnects: int = 5, teleop: Optional[Any] = None, planner: Optional[str] = None) -> None:
        self._gateway = gateway
        self._model = model


        self._planner = planner



        self.teleop = teleop


        self._own_timeout_s = timeout_s
        self._timeout_s = DEFAULT_TIMEOUT_S if timeout_s is None else timeout_s


        self._request_timeout_s: Optional[float] = None
        self._max_reconnects = max_reconnects



        self.contract: Optional[dict] = None






        self._params: Optional[dict] = None


        self._pending_params: Optional[dict] = None







        self._lock = threading.RLock()


        self._trace: Optional[ConnectTrace] = None
        self._connected_once = False
        self.on_trace: Optional[Callable[[dict], None]] = None
        self._worker: Optional[_WorkerTransport] = None
        self._epoch: Optional[int] = None




        self._standby: Optional[_WorkerTransport] = None
        self._standby_epoch: Optional[int] = None
        self._standby_ttl_s = 0.0
        self._standby_seen = 0.0
        self._standby_ask_at: Optional[float] = None
        self._standby_ask_s = 0.0
        self._standby_ask_from: Optional[float] = None
        self._standby_retry_s = 0.0
        self._switched = False
        self._stuck = False
        self._lease_deadline: Optional[float] = None
        self._lease_ttl_s: float = 0.0
        self._renew_again_at = 0.0
        self._renew_misses = 0
        self._renewing = False
        self._closed = False









        self._session = uuid.uuid4().hex






        self._hold = _seat._SeatHold(gateway, model, self._session)
        self._give_back = weakref.finalize(self, _seat._give_back, self._hold)
        _seat._LIVE.add(self)
        self._keepalive_every_s: Optional[float] = None
        self._seat_kept = False
        self._in_line = False
        self._reseating = 0
        self._given_back = 0
        self._waiting_ready = False
        self._kept_at: float | None = None
        self._beat_mono: float | None = None
        self._seat_ttl_s = 60.0
        self._keepalive_stop = threading.Event()
        self._keepalive_thread: Optional[threading.Thread] = None
        self._caller_episode: Optional[str] = None
        self._worker_episode: Optional[str] = None
        self._episode_open = False



        self._rotate: Optional[dict] = None
        self._not_saved_said = False
        self.episode_resets = 0


        self._aliases: dict = {}



        self._numbers: dict[str, int] = {}
        self._held: dict[str, list] = {}
        self._last_seen: dict[str, Any] = {}
        self._stream: Optional[_observe.ObserveStream] = None
        self._stream_to: Optional[_WorkerTransport] = None


        self._plays: dict = {}
        self._said_missing = False


        self._keep = _observe.Keep()


        self._resumed: Optional[tuple[str, _WorkerTransport]] = None

        self._observation_sizes = act_size.Observations(model)



    def post(self, path: str, payload: dict, timeout_s: Optional[float] = None, *,
             rid: Optional[str] = None, metrics: Any = None) -> dict:
        """Route the one act path to the worker, with transparent recovery. Other paths error.

        `rid` is the correlation id for this ONE logical act, minted by the caller. It is held
        constant across the internal 401→reconnect→replay loop below, so a failed attempt and its
        replay land under the same rid on the worker rather than producing an orphan phase per HTTP
        attempt. `metrics` is filled by the worker transport with the last attempt's round trip.
        """
        if not path.startswith("/v1/act") or path.startswith("/v1/act/ready"):


            raise SequencesError(f"DirectConnection does not route POST {path}")
        self._assert_open()
        self._ensure_connected()
        self._maybe_renew()





        deadline = (time.monotonic() + timeout_s) if timeout_s is not None else None

        act_s = timeout_s if timeout_s is not None else self._act_timeout_s()




        busy_until: Optional[float] = None
        attempts = busy = 0


        asked = payload.get("episode_id")




        if "inputs" in payload:
            raise InvalidRequest("act() carries no data: on this policy's worker every input goes through observe(). "
                                 "Hand it to policy.observe(x) first, then call policy.act() - the policy's act function "
                                 "reads what its observations gave it")
        payload["call"] = "act"

        own = self._own_act(asked) if asked is not None else None
        resets = self.episode_resets
        resent = False
        lost = 0
        busy_since: Optional[float] = None
        while True:
            worker = self._current_worker()
            if asked is not None:
                payload["episode_id"] = asked
            self._apply_episode(payload)
            if own is not None and self.episode_resets != resets:

                own, resets = self._own_anew(asked), self.episode_resets
            if own is not None:
                self._observed_act(payload, worker, own)

            if self._params is not None:
                payload["params"] = self._params
            else:
                payload.pop("params", None)
            try:


                stuck_s = worker.stuck_after() if self._standby is not None else None
                worker.chunk_s = self._chunk_s()
                send = worker.post_act if stuck_s is None else self._act_unless_stuck(worker, stuck_s)
                tried = time.monotonic()
                answer = send(payload, timeout_s, rid=rid, metrics=metrics,
                              answer_s=None if timeout_s is not None else act_s)
                if self._resumed is not None:
                    self._resumed_answered()
                if own is not None and payload.get("seq") is not None and self._stream is not None:

                    self._stream.served(payload["episode_id"], payload["seq"] - 1)
                return answer
            except AuthError as exc:





                attempts += 1
                if attempts > self._max_reconnects or self._past(deadline):
                    raise AuthError(
                        "worker kept rejecting the direct secret after "
                        f"{attempts - 1} reconnects",
                        status=exc.status, hint=exc.hint,
                    ) from None
                self._reconnect(worker, backoff_attempt=None)
            except _WorkerGone as exc:




                if exc.waited_s is not None:
                    running_s = worker.act_running(exc.waited_s, rid=rid)
                    if running_s is not None:
                        raise self._still_running(exc.waited_s, running_s) from None



                attempts += 1
                if attempts > self._max_reconnects or self._past(deadline):
                    raise Unavailable(
                        f"worker unreachable after {attempts - 1} reconnect attempts: {exc}",
                        status=503, hint="a robot reaches its worker on one WebSocket (wss): check that this machine's "
                                         "network lets it through",
                    ) from None
                self._reconnect(worker, backoff_attempt=attempts, standby="could not be reached")
            except Conflict as exc:



                if (exc.details.get("reason") == _observe.FRAMES_MISSING and self._resumed is not None
                        and own is not None and self._unkept(payload["episode_id"], exc.details.get("from"), own)):
                    with self._lock:
                        why = self._drop_resumed()
                        if why is not None:
                            self._rotate_episode(standby=why)
                    continue


                if (exc.details.get("reason") == _observe.FRAMES_MISSING and own is not None and not resent
                        and self._stream is not None):
                    resent = True
                    first = exc.details.get("from")
                    first = first if isinstance(first, int) else 0
                    self._say_missing(time.monotonic() - tried, first)
                    _marked.force(self, payload["episode_id"])
                    self._stream.resend(payload["episode_id"], first, act_s)
                    continue


                if exc.details.get("reason") != _EPISODE_LOST or lost:
                    raise
                lost += 1
                self._lose_episode(worker, exc.details.get("cause"))
            except Unavailable as exc:



                if exc.details.get("reason") in ("draining", _COPY_STUCK):
                    attempts += 1
                    if attempts > self._max_reconnects or self._past(deadline):
                        raise
                    ran = exc.details.get("ran_s")
                    why = ("is going away" if exc.details.get("reason") == "draining"
                           else f"was stuck on an act for {ran:g} s" if isinstance(ran, (int, float))
                           else "was stuck on an act")
                    self._reconnect(worker, backoff_attempt=attempts, standby=why,
                                    stuck=exc.details.get("reason") == _COPY_STUCK)
                    continue


                if exc.details.get("reason") in _STATE_GONE and not lost:
                    lost += 1
                    self._lose_episode(worker, exc.details.get("reason"))
                    continue




                if exc.status == 429 and exc.details.get("reason") == _NO_PLACE:
                    attempts += 1
                    if attempts > self._max_reconnects or self._past(deadline):
                        raise
                    self._reseat(worker, attempts)
                    continue





                if exc.status != 429:
                    if lost and exc.warming:




                        raise Unavailable(
                            f"the copy of the policy holding this episode stopped and is starting again ({exc}); the "
                            "robot was not moved on - call act() again and it goes on in a new episode once "
                            "the copy is back", status=exc.status, code=exc.code, body=exc.body,
                            retry_after_s=exc.retry_after_s, request_id=exc.request_id, details=exc.details,
                            warming=True, job_id=exc.job_id) from None
                    raise
                busy += 1
                now = time.monotonic()
                if busy_until is None:
                    busy_until = now + act_s if deadline is None else min(now + act_s, deadline)
                    busy_since = now
                wait = _busy_backoff(busy, exc.retry_after_s)
                if now + wait > busy_until:
                    raise Unavailable(
                        f"worker was busy on {busy} attempts in a row ({exc})",
                        status=429, body=exc.body, retry_after_s=exc.retry_after_s,
                    ) from None
                if busy_since is not None and now + wait - busy_since >= _SAY_BUSY_AFTER_S:

                    busy_since = None
                    warn(f"waiting for an available copy of the policy on its worker: {exc}")
                time.sleep(wait)

    def _unkept(self, episode: str, first: Any, own: tuple) -> bool:
        """Whether `first` - the first observation of `episode` a worker lacks - is before every one this robot still
        keeps of it (its stream's): none it could send again."""
        if not isinstance(first, int) or isinstance(first, bool):
            return False
        oldest = self._stream.oldest(episode) if self._stream is not None else None
        return oldest is None or first < oldest

    def _act_unless_stuck(self, worker: _WorkerTransport, stuck_s: float) -> Callable[..., dict]:
        """worker.post_act, its answer waited for `stuck_s` (_WorkerTransport.stuck_after) on a thread of its own. Past
        that its worker is asked on another connection whether it still runs the act (stuck_probe):
        - no answer in time: the worker is gone, and the act goes to the standby at once - _WorkerGone, which the act's
          loop takes to the switch (_reconnect, _switch);
        - it runs it: the act waits on for its answer, as long as any act may;
        - it does not run it - the act's request, or its answer, still on its way or lost with its connection: the
          worker is there, so the act never goes to the standby for that. Every worker runs an act once by its request
          id: an act that never reached it goes again under that id, on the
          connection the question opened, and one it answered is waited for on its own - and goes again, answered once
          more, when the next question finds it answered still: that connection lost it. At most _RESENDS times, the
          first answer taken.
        A try given up on is left to end by itself, never cut: its connection closes once it does
        (_WorkerTransport.close), and what it answers then is dropped, as what it filled in of its metrics is. Its thread
        is a daemon: a robot's program that ends is not held for that answer.

"""
        def send(payload: dict, timeout_s: Optional[float], *, metrics: Any = None, **kw: Any) -> dict:
            tries: list[tuple[concurrent.futures.Future, Any]] = []

            def go() -> None:
                mine = copy.copy(metrics) if metrics is not None else None
                fut: concurrent.futures.Future = concurrent.futures.Future()
                again = bool(tries)

                def run() -> None:
                    try:
                        fut.set_result(worker.post_act(payload, timeout_s, metrics=mine, again=again, **kw))
                    except BaseException as exc:
                        fut.set_exception(exc)

                tries.append((fut, mine))
                threading.Thread(target=run, daemon=True, name="seq-act").start()

            go()
            began = asked = time.monotonic()
            wait_s: Optional[float] = stuck_s
            says: Optional[str] = None
            while True:
                pending = [f for f, _ in tries if not f.done()]
                if pending:
                    left = None if wait_s is None else max(0.0, asked + wait_s - time.monotonic())
                    concurrent.futures.wait(pending, timeout=left, return_when=concurrent.futures.FIRST_COMPLETED)
                for fut, mine in tries:


                    if fut.done() and not isinstance(fut.exception(), _WorkerGone):
                        if mine is not None:
                            metrics.__dict__.update(mine.__dict__)
                        return fut.result()
                if all(f.done() for f, _ in tries):
                    fut, mine = tries[0]
                    if mine is not None:
                        metrics.__dict__.update(mine.__dict__)
                    return fut.result()
                if wait_s is None or time.monotonic() < asked + wait_s:
                    continue
                says, was = worker.stuck_probe(time.monotonic() - began, kw.get("rid")), says
                asked = time.monotonic()
                if says is None:
                    raise _WorkerGone(f"its worker answered nothing in {stuck_s * 1000:.0f} ms, nor a question on "
                                      "another connection")
                if says == "running":
                    wait_s = None
                elif len(tries) <= _RESENDS and (says == "missing" or says == "answered" and was == "answered"):
                    go()
        return send

    def handshake(self) -> Optional[dict]:
        """Connect now if not yet connected — the same handshake the first act makes — and return what the deployment
        declares of its inputs: nothing since its observations= went (contract 0.5.34), {} once connected."""
        self._assert_open()
        self._ensure_connected()
        return self.contract

    def place(self) -> None:
        """One POST /v1/act/connect now: the robot's ask for a place, as wait_until_ready() sends it when its ready
        poll says the robot holds nothing (`cold`) or waits in line (`queued`) - a poll only looks. Seated on a running
        worker, it returns, the connection to that worker opening behind it (prewarm); a worker started for it, nearest
        it, or its place in line is raised as a first act's connect raises them (Unavailable warming / queued), as is
        anything else. A worker connection it still has holds no seat on the platform's word: it connects anew, as a
        reconnect does.
"""
        self._assert_open()
        with self._lock:
            if self._worker is not None:
                self._worker.gone = True
            self._connect(renew=False)

    def get(self, path: str) -> dict:
        """Catalogue and readiness stay on the gateway — they are control-plane lookups.

        A ready poll only looks: what places a robot - a seat, a worker started for it, a place in line - is its connect
        (place, or its first act's). A poll that names this session keeps alive what the session holds, so it is given
        back as a connect's seat is: at close(), the end of a `with`, collection, exit and SIGTERM / SIGHUP.
        
When the answer asks it (`keepalive`), the place is kept alive while the Policy
        is open, as a connect's seat is - a robot told ready keeps its seat until its first act, however long."""
        self._assert_open()
        placing = path.startswith("/v1/act/ready") and f"session={self._session}" in path
        if placing:

            self._hold.sent = True
            _seat._guard_signals()
        body = self._gateway.get(path)
        if placing:
            self._in_line = isinstance(body, dict) and body.get("status") == "queued"
            self._seat_alive(body, ready=True)



            self._trace_ready_poll(body)
        return body

    @property
    def session(self) -> str:
        """This client's session: what its connects name it by, and its ready polls too, so the platform answers a poll
        for this robot - queued when its deployment is full - rather than for any robot."""
        return self._session

    @property
    def base_url(self) -> str:
        return self._gateway.base_url

    @property
    def open_episode(self) -> Optional[str]:
        """The caller's episode this connection has open - acts sent under it and no end since - else None."""
        with self._lock:
            return self._caller_episode if self._episode_open else None

    def close(self) -> None:




        with self._lock:
            ending = None if self._closed or not self._episode_open else (self._worker, self._worker_episode)
            self._episode_open = False
        if ending is not None and ending[0] is not None and ending[1]:
            ending[0].post_episode_end(ending[1])
        with self._lock:
            if self._closed:
                return
            self._closed = True
            if self._stream is not None:
                self._stream.close()
            if self._worker is not None:
                self._worker.close()
                self._worker = None
            if self._standby is not None:
                self._standby.close()
                self._standby = None

        self._keepalive_stop.set()
        self._give_back()
        self._gateway.close()

    def _move_waits(self) -> bool:
        """Whether the platform told this robot to move and said nothing has room for it yet (its notice's `ready`
        false): the seat keepalive then asks again within seat._MOVE_ASK_S, so the robot moves at the first episode
        boundary after a worker has room - where it heard of that room only at its next beat, every_s on.
        

"""
        if self._closed:
            return False
        rotate = self._rotate
        if isinstance(rotate, dict):
            return rotate.get("ready") is False



        heard = getattr(self._worker, "leaving_since", None)
        return heard is not None and time.monotonic() - heard < _LEAVING_ASK_S

    def _move_ask_now(self) -> bool:
        """Whether its worker has said it is leaving (X-Seq-Leaving) since the last keepalive was sent: the seat
        keepalive asks at once, not seat._MOVE_ASK_S on - its notice an ask sooner. {dev 10-27 22:19:56.5Z on cl3a: its
        worker told it was leaving, the robot asked 3.3 s on}"""
        heard = getattr(self._worker, "leaving_since", None)
        return heard is not None and (self._beat_mono is None or self._beat_mono < heard)

    def _say_missing(self, waited_s: float, first: int) -> None:
        """An act its worker answered 409 frames_missing - the observations before it, from number `first`, never
        reached it - which goes again after them: how long it waited and why, on the debug log every time and said once
        a connection (warnings.warn), as the robot would otherwise only see an act that took longer.

"""
        line = (f"act() waited {waited_s:.1f} s: its worker had not received the observations posted before it (from "
                f"number {first}), so they were sent again, then the act")
        _log.debug("%s", line)
        with self._lock:
            said, self._said_missing = self._said_missing, True
        if not said:
            warn(f"{line}. Said once a connection; every time on the debug log of \"sequence_ai\"")

    def _say_moving(self, notice: dict) -> None:
        """The platform said this robot's worker is leaving: why, and the latest it is moved by, so a move that comes
        mid-episode at that time is never a surprise - said once each time its worker begins to leave, on stderr as the
        seat's notices are (_say_seat_went). It was a UserWarning, shown with the library's file and source line.
        

"""
        print(f"[sequences] {self._model}: {_moving_words(notice)}", file=sys.stderr, flush=True)

    def _say_not_saved(self, said: Any) -> None:
        """The platform says this robot's episodes are to be kept and its account has no room for them: said once, on
        stderr as the seat's notices are, and again should it come back after room was made. A person's demonstrations
        are among them, and a robot's act never fails for it, so nothing else tells whoever runs it. Nothing from a
        platform that says none.
"""
        if not isinstance(said, str) or not said:
            self._not_saved_said = False
        elif not self._not_saved_said:
            self._not_saved_said = True
            print(f"[sequences] {self._model}: {said} (seq account set --storage-limit <GB>, or your Account page)",
                  file=sys.stderr, flush=True)

    def _say_where(self, where: Any) -> None:
        """Where the worker this robot now acts on runs, as the platform names its regions - "US East", never a
        provider's region - and about how far from the robot when no worker nearer it had room: said once each time
        its worker changes, on stderr as the seat's other notices are. A close-loop seat (where["close_loop"]) - a
        running worker a region away the robot still closes its loop on - says it still closes the loop, by the robot's
        own network ("network") or the default round trip ("default"), rather than only that the round trip is longer.
        Nothing from a platform that says none.

"""
        if not isinstance(where, dict) or not isinstance(where.get("region"), str) or not where["region"]:
            return
        far = where.get("far_km")
        km = (f", about {round(float(far), -2):,.0f} km from this robot"
              if isinstance(far, (int, float)) and far > 0 else "")
        loop = where.get("close_loop")
        if loop in ("network", "default"):
            est = "your network's estimate" if loop == "network" else "the default round trip"
            tail = (f"{km}: none in its own region had room, but this worker was already running and "
                    f"by {est} it still closes the loop")
        elif km:
            tail = f"{km}: no worker nearer it had room, so each act's round trip is that much longer"
        else:
            tail = ""
        print(f"[sequences] {self._model}: its worker runs in {where['region']}{tail}", file=sys.stderr, flush=True)



    def _connect(self, *, renew: bool, move: bool = False) -> None:
        """
        One POST /v1/act/connect. Builds (or, on an unchanged secret, keeps) the worker
        transport. Must be called under _lock.

        Warming (503) and OutOfCredit (402) are left to propagate: a cold/zeroed fleet answers
        connect with 503+Retry-After, which the control loop's own warming-wait handles
        (respecting Retry-After, bounded by the startup deadline, resuming when ready); 402 is a
        balance problem the caller must see, not something to retry into a hang. A full deployment
        that queues the robot answers 503 with `details.queue_position`, and the same wait polls it
        (Unavailable.queued); the session id stays the same, so the robot keeps its place in line.
        """







        trace = None
        if not renew:
            trace = self._trace
            if trace is None or trace.done:
                trace = self._trace = ConnectTrace(self._report_trace, reconnect=self._connected_once)
        request = self._connect_request(move=move, again=not renew and self._connected_once)
        t_connect = trace.attempt() if trace is not None else time.monotonic()
        try:
            body = self._gateway.post("/v1/act/connect", request, timeout_s=self._timeout_s)
        except Exception as exc:
            if isinstance(exc, Unavailable):
                self._in_line = exc.queued
            if trace is not None:
                if isinstance(exc, Unavailable) and (exc.warming or exc.queued):
                    trace.wait(queued=exc.queued)
                else:
                    self._trace = None
                    trace.failed(error_of(exc), stage=_refused_in(exc))
            raise
        self._in_line = False
        connect_ms = (time.monotonic() - t_connect) * 1000.0
        if trace is not None:
            trace.connected(t_connect, body.get("timing") if isinstance(body, dict) else None)
        try:
            self._connect_answer(body, renew=renew, move=move, connect_ms=connect_ms)
        except Exception as exc:
            if trace is not None:
                self._trace = None
                trace.failed(error_of(exc), stage="gateway")
            raise
        if trace is not None:

            self._trace, self._connected_once = None, True
            if self._worker is not None:
                self._worker.connect_trace = trace

    def connect_stopped(self, exc: Optional[BaseException]) -> None:
        """The robot's wait for a worker ended with none - given up (`exc`, what it was told), or stopped by its robot
        (None, interrupt()): the trace of the connect under way ended so, failed in the stage it waited in, or dropped
        unsaid."""
        with self._lock:
            trace, self._trace = self._trace, None
        if trace is None:
            return
        if exc is None:
            trace.dropped()
        else:
            trace.failed(error_of(exc))

    def _trace_ready_poll(self, body: Any) -> None:
        """Begin (or go on with) the connect trace on a ready poll that names this session - the robot's first ask for a
        worker.

        WHY: wait_until_ready() polls /v1/act/ready before its connects - the one that places the robot, the one that
        opens its connection once it is ready - and a trace begun in _connect left the robot's wait for a starting
        worker out of `seq policy status`'s "how fast to the first answer" - it read the connect and first act alone
        (hbprobe waited to {"t": 106.8} yet status read p50 756 ms). Begun here, the wait is counted (cold_start /
        queue) while a poll says a worker starts for the robot or it waits in line; _connect (place, connect_ahead, or
        the first act) reuses this same trace (self._trace, not done), so total_ms spans the first ask to the first act.
        A robot that gives up or is interrupted mid-wait ends it in the stage it waited in (connect_stopped,
        waits._gave_up); one already on a worker is not a new connect.

        
"""
        with self._lock:
            if self._closed or (self._worker is not None and not self._worker.gone):
                return
            if self._trace is None or self._trace.done:
                self._trace = ConnectTrace(self._report_trace, reconnect=self._connected_once)



            said = body if isinstance(body, dict) else {}
            if said.get("ready") is not True and said.get("status") != "cold":
                self._trace.wait(queued=said.get("status") == "queued")

    def _report_trace(self, report: dict) -> None:
        """A connect's trace ended: its report to the Policy's reporter (on_trace), best effort."""
        said = self.on_trace
        if said is not None:
            said(report)

    def _connect_request(self, *, move: bool, again: bool = False) -> dict:
        """The body of one POST /v1/act/connect, the session marked as having reached it. Under _lock. `again`: a
        connect, not a renewal, of a robot that was connected before - one whose seat went with a worker that went away
        is then seated by the platform as a robot moving off it (a free seat beside robots first), never as a new one."""
        request = {"model": self._planner or self._model, **({"policy": self._model} if self._planner else {}),
                   "session": self._session, "standby": True, **({"move": True} if move else {}),
                   **({"switched": True} if self._switched else {}),


                   **({"stuck": True} if self._stuck else {}),
                   **({"again": True} if again else {}),

                   **({"teleop": True} if self.teleop else {})}

        self._hold.sent = True
        _seat._guard_signals()
        return request

    def _same_worker(self, body: Any) -> bool:
        """Whether a connect's answer names the worker connection this robot already has: the same lease epoch, address
        and secret."""
        try:
            return (self._worker is not None and self._epoch is not None and isinstance(body, dict)
                    and (body.get("lease") or {}).get("epoch") == self._epoch
                    and self._worker.same(body["worker_url"], body["direct_secret"]))
        except (KeyError, TypeError, AttributeError):
            return False

    def _connect_answer(self, body: Any, *, renew: bool, move: bool, connect_ms: float) -> None:
        """What a connect answered (_connect), taken: its contracts, its word that the worker is leaving, its parameters,
        the seat's keepalive - and the worker connection, kept on an unchanged secret, else built anew. Under _lock."""
        self._take_contract(body)
        was = self._rotate
        self._rotate = body.get("rotate") if isinstance(body, dict) else None
        if isinstance(self._rotate, dict) and not was:
            self._say_moving(self._rotate)
        self._say_not_saved(body.get("not_saved") if isinstance(body, dict) else None)
        self._take_params(dict(body["params"]))
        self._take_request_timeout(body.get("request_timeout_s"))


        try:
            worker_url = body["worker_url"]
            direct_secret = body["direct_secret"]
            fingerprint = body["cert_fingerprint"]
            lease = body.get("lease") or {}
            epoch = lease.get("epoch")
            ttl_s = float(lease.get("ttl_s") or 0.0)
        except (KeyError, TypeError, ValueError):


            raise SequencesError("malformed /v1/act/connect response") from None



        self._seat_alive(body)
        self._take_standby(body.get("standby"))
        self._plan_standby_ask(body.get("standby_retry_s"))
        self._switched = self._stuck = False




        secret_unchanged = (renew and self._worker is not None and epoch is not None
                            and epoch == self._epoch)



        stayed = move and self._same_worker(body)
        if secret_unchanged or stayed:
            self._set_lease(ttl_s)
            return

        new_worker = _WorkerTransport(worker_url, direct_secret, fingerprint, self._timeout_s, session=self._session,
                                      teleop=self.teleop)
        new_worker.connect_ms = connect_ms

        new_worker.prewarm()
        old = self._worker






        kept = (old is not None and epoch is not None and epoch == self._epoch
                and getattr(old, "_base", None) == str(worker_url).rstrip("/"))
        self._worker = new_worker
        self._epoch = epoch
        self._set_lease(ttl_s)
        if not kept:
            self._say_where(body.get("where"))
        if old is not None:

            if not kept:
                self._rotate_episode(was if isinstance(was, dict) else None)
            try:
                old.close()
            except Exception:
                pass

    def _take_standby(self, said: Any) -> None:
        """The standby copy a connect named (`standby`: its worker's address, secret, certificate and lease, as the
        worker's own), its connection opened at once (prewarm) - the one kept is kept on the same address and secret,
        another closed; none named, none kept. A malformed one is none: its body carries a secret, so it is never said.
        Under _lock."""
        old, fresh = self._standby, None
        if isinstance(said, dict):
            try:
                url, secret, fingerprint = said["worker_url"], said["direct_secret"], said["cert_fingerprint"]
                lease = said.get("lease") or {}
                epoch, ttl_s = lease.get("epoch"), float(lease.get("ttl_s") or 0.0)
            except (KeyError, TypeError, ValueError):
                said = None
            else:
                if old is not None and not old.gone and old.same(url, secret) and epoch == self._standby_epoch:
                    fresh = old
                else:
                    fresh = _WorkerTransport(url, secret, fingerprint, self._timeout_s, session=self._session)
                    fresh.prewarm()
                    self._standby_seen = time.monotonic()
                self._standby_epoch, self._standby_ttl_s = epoch, ttl_s
        self._standby = fresh
        if fresh is not None:
            self._keep.s = _observe.KEEP_SERVED_S
        if old is not None and old is not fresh:
            try:
                old.close()
            except Exception:
                pass

    def _plan_standby_ask(self, retry: Any) -> None:
        """When to ask again for the standby a connect could not hold (its `standby_retry_s`, the platform's pace): a
        standby held, or none said - a deployment that keeps no spare worker - no ask, the gap
        over; said, the ask already planned stands (each ask plans the next: _renew_ahead), else one `retry` seconds on,
        the gap begun now unless a let-go began it. Under _lock."""
        if self._standby is not None or isinstance(retry, bool) or not isinstance(retry, (int, float)) or retry <= 0:
            self._standby_ask_at, self._standby_ask_s, self._standby_ask_from = None, 0.0, None
            return
        self._standby_retry_s = float(retry)
        if self._standby_ask_at is None:
            now = time.monotonic()
            self._standby_ask_from = self._standby_ask_from or now
            self._standby_ask_s = self._standby_retry_s
            self._standby_ask_at = now + self._standby_ask_s

    def _keep_standby(self) -> None:
        """From the seat keepalive's thread: the standby's stream kept open - a /ping each _STANDBY_PING_S, so no
        idle timeout between here and its worker closes it before an act needs it - and one that does not answer let go
        (the next connect names another). Never raises."""
        with self._lock:
            standby = self._standby
            if self._closed or standby is None or time.monotonic() - self._standby_seen < _STANDBY_PING_S:
                return
        alive = standby.alive()
        with self._lock:
            if self._standby is not standby:
                return
            if alive:
                self._standby_seen = time.monotonic()
                return
            self._standby = None

            now = time.monotonic()
            self._standby_retry_s = self._standby_retry_s or _STANDBY_ASK_S
            self._standby_ask_from, self._standby_ask_s, self._standby_ask_at = now, self._standby_retry_s, now
        standby.close()

    def _switch(self, stale: _WorkerTransport, why: str) -> bool:
        """The worker an act was on (`stale`) stopped answering - `why`, in words that name no machine - so the act goes
        to the standby copy at once, its connection already open: no connect between, the platform told after it, in
        the background (_report_switch). The robot's episode goes on there under its id when the standby reads its state
        back (_resumes_on, plan 99 U8), else in a new one, as after a reconnect to another worker: a copy that reads
        nothing back holds none of this one's state. False when there is no standby to go to: the act's reconnect
        goes through the platform, as before. True too when another thread already moved on from `stale`: the act goes
        again on what it moved to. A standby that has not said it reads an episode back is asked once first (/ping,
        _SWITCH_ASK_S at most): it says so on each answer, and the keepalive asks it only each _STANDBY_PING_S, so one
        whose worker took its deployment's standby setting after the robot took it (a deploy's first worker, with
        buffer_workers raised live) had the episode go on as a new one.
"""
        with self._lock:
            asked = None if self._closed or self._worker is not stale else self._standby
        if asked is not None and not asked.gone and asked.resumes is not True:
            asked.alive(timeout_s=_SWITCH_ASK_S)
        with self._lock:
            if self._closed:
                return False
            if self._worker is not stale:
                return True
            standby = self._standby
            if standby is None or standby.gone:
                return False
            self._standby = None
            self._worker, self._epoch = standby, self._standby_epoch
            self._set_lease(self._standby_ttl_s)
            self._switched = True
            if self._resumes_on(standby):
                self._resume_episode(standby, why)
            else:
                self._rotate_episode(standby=why)
            _marked.force(self)
        try:
            stale.close()
        except Exception:
            pass
        threading.Thread(target=self._report_switch, daemon=True, name="seq-standby-switch").start()
        return True

    def _report_switch(self) -> None:
        """The platform told that this robot's act went to its standby (a connect, `switched`), sent with no lock held:
        it moves the robot's seat there and names another standby. An answer on the worker the robot is on now is taken
        - its lease, its next standby; any other, or none, is left for the next renewal, which says `switched` again
        until one is taken. Never raises."""
        with self._lock:
            if self._closed or self._renewing or not self._switched:
                return
            worker = self._worker
            request = self._connect_request(move=False)
            self._renewing = True
        body, connect_ms = None, 0.0
        try:
            t_connect = time.monotonic()
            body = self._gateway.post("/v1/act/connect", request,
                                      timeout_s=min(float(self._timeout_s or _RENEW_AHEAD_TIMEOUT_S),
                                                    _RENEW_AHEAD_TIMEOUT_S))
            connect_ms = (time.monotonic() - t_connect) * 1000.0
        except Exception:
            pass
        with self._lock:
            self._renewing = False
            if body is None or self._closed or self._worker is not worker or not self._same_worker(body):
                return
            try:
                self._connect_answer(body, renew=True, move=False, connect_ms=connect_ms)
            except Exception:
                pass

    def _chunk_s(self) -> Optional[float]:
        """How long one answer plays, its valid steps at hz as connect said them; None when it said neither."""
        hz, valid = self._plays.get("hz"), self._plays.get("action_chunk_valid_len")
        if isinstance(hz, bool) or not isinstance(hz, (int, float)) or hz <= 0:
            return None
        if isinstance(valid, bool) or not isinstance(valid, int) or valid < 1:
            return None
        return valid / float(hz)

    def chunk_ends(self) -> Optional[float]:
        """When the answer the robot plays runs out, on time.monotonic(): its act's send time plus its valid steps at
        hz - what an act sent now tells the worker is left of it (X-Seq-Chunk-Left-Ms); None before an answer on this
        worker, or where the policy declares no valid length or hz (stale.py)."""
        chunk_s = self._chunk_s()
        asked = getattr(self._worker, "_playing_asked", None)
        return None if chunk_s is None or asked is None else asked + chunk_s

    def heartbeat(self, body: dict) -> None:
        """A heartbeat on the stream to the worker this robot holds now (heartbeat.py): none before a worker, nor after
        close."""
        worker = self._worker
        if worker is not None and not self._closed:
            worker.post_heartbeat(body)

    def note_outside(self, ms: float) -> None:
        """An act this robot's worker answered spent `ms` outside it (its time less the worker's handler_ms): into the
        window of the worker's connection, which its next acts tell the worker."""
        worker = self._worker
        if worker is not None:
            worker.note_outside(ms)

    @property
    def steps_played(self) -> Optional[int]:
        """How many steps the robot plays between asking for an answer and needing it, as the policy declares it - its
        action_chunk_valid_len less its action_chunk_replan_at (capacity.wait_steps) - for the act's report, over hz the
        time the answer must arrive in; None when it declares no valid length, asks at its last valid step (its robot
        waits for every answer), or before the connect that says it."""
        from .capacity import wait_steps

        steps = wait_steps(self._plays.get("action_chunk_valid_len"), self._plays.get("action_chunk_replan_at"))
        return steps or None

    def _take_request_timeout(self, said) -> None:
        """What the deployment allows one act, in seconds, as its connect or a keepalive says it (none: not said): an
        act waits that long and a little more, so the worker's own 504 at that deadline is what the robot reads."""
        try:
            value = float(said or 0.0)
        except (TypeError, ValueError):
            value = 0.0
        self._request_timeout_s = value if value > 0 else None

    def _take_contract(self, body: dict) -> None:
        """Keep what connect returned of the policy's declarations: how its answers play (hz, action_chunk_valid_len,
        action_chunk_replan_at, contract 0.5.35) and how long its robot waits for an answer where it sets that
        (max_wait_for_batch, contract 0.5.45) - what late.py holds an answer to."""
        if not isinstance(body, dict):
            return
        self._plays = {k: body[k] for k in ("hz", "action_chunk_valid_len", "action_chunk_replan_at",
                                            "max_wait_for_batch") if body.get(k)}
        self.contract = {}

    def _ensure_connected(self) -> None:
        with self._lock:
            if (self._worker is None or self._worker.gone) and not self._closed:
                self._connect(renew=False)

    def connect_ahead(self, *, wait: bool = False, wait_s: Optional[float] = None,
                      stop: Optional[threading.Event] = None) -> Optional[NotOpen]:
        """
        Connect now, in the background, when nothing is connected - the platform connect, then the worker's connection
        opened (prewarm) - so a first act after Policy.wait_until_ready() waits for neither: on dev a connect and the
        handshake behind it took 2-4 s. Best effort: what fails here is the first act's to meet, as it would have been;
        an act that comes while this runs waits for it (_lock), never a second connect.



        `wait`: wait until the connection to the worker is open - the platform connect answered, the TLS handshake done
        and the worker's certificate checked - and say whether it is: None once it is, else a NotOpen (which stage, what
        it met or that it was still under way). For at most this connection's own timeout (connect(timeout_s=), 30 s by
        default) - what a first act would have waited for it - or `wait_s` when that is shorter. Nothing is raised and
        nothing is cut short: what failed, the first act meets as it would have (it connects, or opens a connection,
        again); what was still under way goes on, and the first act waits for it. Without `wait` this returns at once.
        `stop` (the robot's interrupt), once set, ends the wait: still under way, which the caller reads as interrupted.
        Before, wait_until_ready() returned as this began, so an act sent at once waited out the rest; now the robot is
        told ready once its connection is open.
        


        """
        if self._closed:
            return None
        t0 = time.monotonic()

        limit = self._timeout_s if wait_s is None else min(wait_s, self._timeout_s)
        worker = self._worker
        if worker is None or worker.gone:

            finished, failed = threading.Event(), []

            def _run() -> None:
                try:
                    self._ensure_connected()
                except Exception as exc:
                    failed.append(exc)
                finally:
                    finished.set()

            threading.Thread(target=_run, daemon=True, name="seq-connect-ahead").start()
            if not wait:
                return None
            if not _wait_set(finished, limit, stop):
                return NotOpen("connect", None, time.monotonic() - t0)
            if failed:


                exc = failed[0]
                said = exc.message if isinstance(exc, SequencesError) else type(exc).__name__
                return NotOpen("connect", said, time.monotonic() - t0)
            worker = self._worker
            if worker is None:
                return None
        elif not wait:
            return None

        why = worker.wait_open(limit - (time.monotonic() - t0), stop)
        if why is None:
            return None
        return NotOpen("open", None if why == _STILL_OPENING else why, time.monotonic() - t0)

    def _reconnect(self, stale: _WorkerTransport, *, backoff_attempt: Optional[int],
                   standby: Optional[str] = None, stuck: bool = False) -> None:
        """
        Reconnect through the gateway, unless another thread already did it for this worker.

        `stale` is the transport the caller was using when it failed. If it is no longer the
        current one, a concurrent caller has already reconnected and this thread just retries on
        the fresh transport — so a burst of failures from many robots on one dead worker becomes
        one reconnect, not a storm.

        `standby`: why the worker failed, when it stopped answering or is going away - the act then goes to the
        standby copy the platform keeps it, at once and with no backoff, when there is one (_switch). A worker that
        rotated its secret (401) is the same worker: reconnected through the gateway, as before. `stuck`: its copy was
        stuck on an act (503 copy_stuck) - with no standby, its connect says so, and the platform seats it elsewhere.
        """
        if standby is not None and self._switch(stale, standby):
            return
        if backoff_attempt is not None:
            time.sleep(min(2.0, 0.1 * (2 ** (backoff_attempt - 1))))
        with self._lock:
            if self._closed:
                raise SequencesError("connection was closed during reconnect")
            if self._worker is not stale:
                return
            self._stuck = self._stuck or stuck
            try:
                self._connect(renew=False)
                _marked.force(self)
            except BaseException:




                stale.gone = True
                raise

    def _driven_by_a_person(self) -> bool:
        """A person drives this robot (connect(teleop=True)): act() answers from the person's chunks and sends nothing to
        its worker, yet the robot is in a run - its lease renewed ahead as an acting robot's is, so the act its model
        answers once the person hands it back waits on no renewal.
"""
        teleop = self.teleop
        return teleop is not None and getattr(teleop, "driver", None) == "human"

    def _renew_ahead(self) -> None:
        """From the seat keepalive's thread, once the lease's renewal is _RENEW_AHEAD_BEATS beats away and the robot is in
        a run (it acted within _RENEW_AHEAD_ACTED_S): renewed now, its connect sent with no lock held, so the act that
        reaches the deadline finds it done instead of waiting on it, held up as long as that connect took - and, while
        the platform could not hold this robot a standby, once its ask is due (_plan_standby_ask), the next one planned
        whatever this one's answer: at the platform's pace while the gap is young (_STANDBY_FAST_S), else twice as far
        on as the last. Only an answer on the same worker is taken here - the lease moved
        on, and what the platform says with it; anything else (another worker, a refusal, the robot put in line, no
        answer) is left for that act's renewal, as before. Not between episodes while the robot is to move: that act's
        renewal is its move. Never raises.
        
"""
        with self._lock:
            now = time.monotonic()
            ahead = _RENEW_AHEAD_BEATS * (self._keepalive_every_s or 20.0)
            worker = self._worker


            asks = (self._standby is None and self._standby_ask_at is not None
                    and now >= self._standby_ask_at - (self._keepalive_every_s or 20.0) / 2)
            if (self._closed or self._renewing or worker is None or self._lease_deadline is None
                    or (now < self._lease_deadline - ahead and not asks) or now < self._renew_again_at
                    or (self._rotate is not None and not self._episode_open)
                    or not (worker.acted_within(_RENEW_AHEAD_ACTED_S) or self._driven_by_a_person())):
                return
            if asks:
                if self._standby_ask_from is not None and now - self._standby_ask_from < _STANDBY_FAST_S:
                    self._standby_ask_s = self._standby_retry_s or _STANDBY_ASK_S
                else:
                    self._standby_ask_s = min(self._standby_ask_s * 2, max(self._standby_ask_s, self._lease_ttl_s))
                self._standby_ask_at = now + self._standby_ask_s
            request = self._connect_request(move=False)
            self._renewing = True
        body, connect_ms = None, 0.0
        try:
            t_connect = time.monotonic()
            body = self._gateway.post("/v1/act/connect", request,
                                      timeout_s=min(float(self._timeout_s or _RENEW_AHEAD_TIMEOUT_S),
                                                    _RENEW_AHEAD_TIMEOUT_S))
            connect_ms = (time.monotonic() - t_connect) * 1000.0
        except Exception:
            pass
        with self._lock:
            self._renewing = False
            if body is None or self._closed or self._worker is not worker or not self._same_worker(body):
                return
            try:
                self._connect_answer(body, renew=True, move=False, connect_ms=connect_ms)
            except Exception:
                pass

    def _maybe_renew(self) -> None:
        """Proactively renew before the lease expires, so a long session never blips on a 401. A robot the platform
        asked to move, with no episode open, moves on this renewal.

        A renewal the gateway cannot answer just now - unreachable, erring, or warming because the worker this robot
        holds did not answer the gateway's own look - leaves the robot acting on that worker, which answers its acts
        directly and checks the direct secret, not the lease: it is tried again after the answer's Retry-After,
        doubling while it keeps failing (_RENEW_AGAIN_S to _RENEW_AGAIN_MAX_S). Raised, it ended a run in flight on the
        gateway's blip, a run raising a warming answer by design. Anything else - out of credit, put in line, refused -
        raises as ever.
        
"""
        with self._lock:
            now = time.monotonic()
            if (self._lease_deadline is None or self._worker is None or now < self._lease_deadline
                    or now < self._renew_again_at or self._renewing):
                return
            try:
                self._connect(renew=True, move=self._rotate is not None and not self._episode_open)
            except (Unavailable, InternalError) as exc:
                if isinstance(exc, Unavailable) and exc.queued:
                    raise
                self._renew_misses += 1
                wait = max(float(exc.retry_after_s or 0.0), _RENEW_AGAIN_S) * 2 ** (self._renew_misses - 1)
                self._renew_again_at = time.monotonic() + min(wait, _RENEW_AGAIN_MAX_S)
                if self._renew_misses == 1:
                    _log.warning("the lease renewal was not answered (%s); acting on, and asking again", exc)



    @staticmethod
    def _past(deadline: Optional[float]) -> bool:
        return deadline is not None and time.monotonic() >= deadline

    def _act_timeout_s(self) -> float:
        """How long an act waits for its answer: the caller's connect(timeout_s=), else what its deployment allows one
        act and _ANSWER_MARGIN_S more (the worker answers 504 at that deadline), else DEFAULT_TIMEOUT_S."""
        if self._own_timeout_s is not None:
            return self._own_timeout_s
        if self._request_timeout_s is not None:
            return self._request_timeout_s + _ANSWER_MARGIN_S
        return DEFAULT_TIMEOUT_S

    def _still_running(self, waited_s: float, running_s: float) -> Unavailable:
        """The act got no answer in `waited_s` and its worker still runs it (`running_s` so far): what to say instead of
        sending it again, with what bounds the wait and how to lengthen it."""
        allowed = self._request_timeout_s
        if allowed is not None and self._own_timeout_s is not None and allowed > self._own_timeout_s:
            hint = (f"its deployment allows an act {allowed:g} s, and "
                    f"connect(timeout_s={self._own_timeout_s:g}) waited less: connect without timeout_s waits that long")
        elif allowed is not None:
            hint = (f"its deployment allows an act {allowed:g} s and its worker answers 504 then - the platform's limit, "
                    f"ten times the slowest p95 its version's check measured, never under 300 s nor over an hour")
        else:
            hint = (f"its deployment says no request timeout, so an act waits {DEFAULT_TIMEOUT_S:g} s: connect(timeout_s="
                    f"...) waits longer")
        return Unavailable(
            f"the act got no answer in {waited_s:.0f} s, and its worker is still running it ({running_s:.0f} s so far): "
            f"it was not sent again, which would run it twice",
            status=504, code="timeout", hint=hint,
            details={"reason": "act_still_running", "waited_s": round(waited_s, 1), "running_s": running_s,
                     "request_timeout_s": allowed})

    def _current_worker(self) -> _WorkerTransport:
        with self._lock:
            if self._worker is None:
                raise SequencesError("no worker connection")
            return self._worker

    def _set_lease(self, ttl_s: float) -> None:
        self._lease_ttl_s = ttl_s
        self._renew_misses, self._renew_again_at = 0, 0.0
        if ttl_s > 0:


            lead = min(30.0, max(1.0, ttl_s * 0.2))
            self._lease_deadline = time.monotonic() + max(0.0, ttl_s - lead)
        else:
            self._lease_deadline = None

    def _assert_open(self) -> None:
        if self._closed:
            raise SequencesError("this connection is closed; open a new one with connect()")


def _refused_in(exc: BaseException) -> str:
    """The stage a connect the gateway answered with no seat stopped in: `auth` - its key refused, its account out of
    credit or over its requests a minute - `place` - its deployment missing, stopped or refusing it - else `gateway`:
    not reached, or erring."""
    status = getattr(exc, "status", None)
    if status in (401, 402, 403, 429):
        return "auth"
    if status in (404, 409, 422):
        return "place"
    return "gateway"

