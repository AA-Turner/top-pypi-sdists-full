"""A live run's console log, shipped while the run is alive (plan item (h), T34).

WHY. Output capture keeps everything a run prints as ``probe/run.log``, but
uploads it only when the run ends (:mod:`probe.sdk.outputs`). A three-day job
showed nothing of its console until then, and a whole-pod death could end it
with nothing uploaded. This ships the log WHILE the run is alive, to
``POST /v1/runs/{id}/log-chunks``, for the run page's Logs panel. The final
artifact is unchanged: it stays the durable copy, and this is best effort.

HOW. The output helper (:mod:`probe.sdk.logcapture`) already reads every byte
the program writes. Given a ``<log>.live/`` directory at start it also appends
them to 1 MiB segment files there, never holding more than 16 MiB unsent. A
:class:`LogStreamer` thread in the process that OWNS the tee (the training
process for ``probe.init()``, the launcher for ``probe exec``) wakes every
``PROBE_LOG_STREAM_SEC`` (15) seconds and ships what is ready:

* COMPLETE LINES ONLY. A partial last line is held back while it is under
  ``MAX_PARTIAL_LINE_BYTES`` -- a credential cannot straddle a newline, so a
  token the program was half-way through printing is never sent in halves the
  gate could not recognise. Past that (a progress bar that never writes a
  newline, a minified JSON dump) it is cut at a redraw or a space, else at the
  size limit -- but NEVER inside a run of token-shaped characters: the run is
  held back whole for the next chunk, and one too long to hold (past
  ``MAX_TOKEN_RUN_BYTES``) is withheld, with a line saying so. The chunk after
  such a cut is redacted together with the text before it, so a key name and
  its value on either side of the cut are still seen as one.
* A PRIVATE KEY BLOCK WHOLE. The gate recognises a PEM block only with its END
  line, so an unterminated one is held back (up to ``MAX_PEM_HOLD_BYTES``);
  one that never ends is withheld, with a line saying so, until it does. After
  a GAP the stream may resume inside a block whose BEGIN was dropped: an END
  seen before any BEGIN withholds everything up to it.
* REDRAWS COLLAPSED: a line a ``\\r`` progress bar rewrote ships as its last
  frame, as the terminal showed it. A chunk cut at a redraw keeps its trailing
  ``\\r``, so the next chunk's first frame replaces it instead of joining it.
* REDACTED by the same function as the final log (`outputs.redact_log_text`);
  text holding a credential it cannot replace is withheld, its place kept.

BOUNDED CPU. The text is cleaned twice, in the TRAINING process, beside the
GIL: here by the final log's redaction, then by the transport's own scrub of
every request body (`transport.Transport.request`). The scrub stays: this
redaction does not do all it does (short vendor-prefixed tokens, values under
credential key names, embedded JSON), so skipping it would lose coverage.
Measured (process CPU time) on dense training output -- step, loss and path
lines -- 256 KiB costs ~0.5 s of redaction plus ~0.4 s of scrub: ~1 s of CPU
per wake-up, ~7% of one core at the 15 s default (plain text ~0.2 s). So one
wake-up ships at most ``PASS_RAW_BYTES`` of raw output -- no chunk takes it
past that -- and a backlog past ``MAX_BACKLOG_BYTES`` skips ahead to the
newest output: the live view is for what the run is doing NOW; the final
artifact keeps the head and the tail. A skip is a jump in offsets, marked as a
gap by the server.

DELIVERY is a direct POST, NOT a journal op: a live view that arrives after the
run ended has no reader, and the journal's durability is for the final log.
Positions make it safe to repeat: every chunk carries its raw offset, the
server ignores one it already covers and answers where the stream continues,
and a failed POST is retried with the IDENTICAL body (backoff from
`durable.RETRY_BACKOFF`, and never sooner than a 429's ``retry_after``). A
segment is deleted once everything in it is sent; the cursor is kept on disk,
so a recovery after a hard death resumes from it, as the attempt the dead
process recorded (its write epoch: a newer attempt's run refuses it). A log
name whose spool survives is never reserved again (`outputs.reserve_log_path`).

WHO STREAMS. Rank 0 only by default (``PROBE_LOG_STREAM=rank0``): 608 ranks
each posting every 15 s would be ~40 requests a second for logs nobody reads
side by side. ``all`` streams every rank, each its own stream ``run.rank<N>``
whatever its log is called (under ``mpirun`` every host's log is
``probe/run.log``, and one shared stream name would make the hosts' chunks
cover each other), ``0`` streams nothing. A server that does not declare
``run_log_stream`` gets nothing: no spool, no request; the answer (a failure
or a timeout too) is kept for the process, so only the first run waits for it.
"""

from __future__ import annotations

import os
import re
import shutil
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable

from probe._compat import StrEnum

from . import errors
from .logcapture import list_segments, live_dir, read_eof

FEATURE = "run_log_stream"
MODE_ENV = "PROBE_LOG_STREAM"
INTERVAL_ENV = "PROBE_LOG_STREAM_SEC"
DEFAULT_INTERVAL_SECONDS = 15.0
#: The shortest ``PROBE_LOG_STREAM_SEC`` honoured: a smaller one is raised to it.
MIN_INTERVAL_SECONDS = 1.0
#: A partial line held back for its newline, and a private key block held
#: back for its END line, at most.
MAX_PARTIAL_LINE_BYTES = 64 * 1024
MAX_PEM_HOLD_BYTES = 16 * 1024
#: Raw bytes one POST covers, one wake-up ships, and the last pass ships.
MAX_CHUNK_RAW_BYTES = 256 * 1024
PASS_RAW_BYTES = 256 * 1024
FINAL_RAW_BYTES = 1024 * 1024
#: Unsent output past which a wake-up skips to the newest ``PASS_RAW_BYTES``.
MAX_BACKLOG_BYTES = 1024 * 1024
#: How long opening a run may wait to learn whether the server takes a live log.
FEATURE_CHECK_SECONDS = 2.0
#: What a close gives the last lines: at most this, and at most
#: ``FINAL_FLUSH_SHARE`` of what is left of its budget -- the outputs sweep
#: after it needs the rest.
FINAL_FLUSH_SECONDS = 5.0
FINAL_FLUSH_SHARE = 0.25
#: How long a stop waits past its budget for a POST already in flight.
STOP_GRACE_SECONDS = 0.5
#: A forced cut never splits a run of the bytes a credential is made of (the
#: gate's `_SECRET_CHARS`, plus `.` and `~` for JWTs and bearer values)...
_TOKEN_RUN = re.compile(rb"[A-Za-z0-9+/=_.~-]*")
#: ...unless the run is longer than this -- past the gate's longest opaque
#: value (a 16 KiB base64 run) -- and it is withheld instead.
MAX_TOKEN_RUN_BYTES = 20 * 1024
#: The text before a forced cut that the next chunk is redacted with.
SEAM_CONTEXT_CHARS = 1024
#: One POST, the transport's own retries and Retry-After waits included, and
#: never past the pass's deadline (a close, a recovery's budget).
POST_TIMEOUT_SECONDS = 10.0
#: Retry after a failed POST: 2 s doubling to 5 min (`durable.RETRY_BACKOFF`).
_BACKOFF_START, _BACKOFF_CAP = 2.0, 300.0
CURSOR_NAME = "cursor"

_OFF = frozenset({"0", "false", "no", "off", "none"})
_RANK_ENVS = ("RANK", "SLURM_PROCID", "OMPI_COMM_WORLD_RANK", "PMI_RANK")
_STREAM_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
#: The gate's own boundaries for a private key block (tap_core/secrets.py).
_PEM_BEGIN = re.compile(rb"-----BEGIN[ A-Z0-9]{0,30}PRIVATE KEY(?: BLOCK)?-----")
_PEM_END = re.compile(rb"-----END[ A-Z0-9]{0,30}PRIVATE KEY(?: BLOCK)?-----")
_PEM_WITHHELD = "[probe: a private key block was withheld from the live log]\n"
_PEM_RESUMED = "[probe: the live log resumed inside a private key block; it was withheld]\n"
_WITHHELD = "[probe: {n:,} bytes of output withheld: they held a credential Probe could not redact]\n"
_RUN_WITHHELD = "[probe: a long unbroken run of output was withheld from the live log]"


class Mode(StrEnum):
    """``PROBE_LOG_STREAM``."""

    RANK0 = "rank0"
    ALL = "all"
    OFF = "0"


def mode() -> Mode:
    raw = (os.environ.get(MODE_ENV) or "").strip().lower()
    if raw in _OFF:
        return Mode.OFF
    if raw == Mode.ALL:
        return Mode.ALL
    return Mode.RANK0  # the default, and what an unknown value means


def global_rank() -> int | None:
    """This process's rank in a distributed job, or None outside one."""
    for name in _RANK_ENVS:
        value = (os.environ.get(name) or "").strip()
        if value.isdigit():
            return int(value)
    return None


def wanted_here() -> bool:
    chosen = mode()
    if chosen is Mode.OFF:
        return False
    return chosen is Mode.ALL or global_rank() in (None, 0)


def interval_seconds() -> float:
    raw = (os.environ.get(INTERVAL_ENV) or "").strip()
    try:
        value = float(raw) if raw else DEFAULT_INTERVAL_SECONDS
    except ValueError:
        return DEFAULT_INTERVAL_SECONDS
    if value <= 0:
        return DEFAULT_INTERVAL_SECONDS
    return max(value, MIN_INTERVAL_SECONDS)


def stream_for(log_name: str) -> str:
    """``probe/run.rank3.log`` -> ``run.rank3``: the stream is the name the
    final artifact has, without the folder and the extension -- except under
    ``PROBE_LOG_STREAM=all`` with a known rank, where it is ``run.rank<N>``
    whatever the log is called: every host of an ``mpirun`` job logs as
    ``probe/run.log``, and the stream names one process across the job."""
    name = log_name.rsplit("/", 1)[-1]
    if name.endswith(".log"):
        name = name[: -len(".log")]
    if not _STREAM_NAME.fullmatch(name):
        name = "run"
    rank = global_rank()
    if mode() is Mode.ALL and rank is not None and not _RANKED.search(name):
        name = f"{name.split('.', 1)[0]}.rank{rank}"
    return name


_RANKED = re.compile(r"\.rank\d+$")
#: `server_accepts`' answers for this process, by server; and the checks still
#: in flight (a timed-out one is never waited on twice).
_ACCEPTS: dict[str, bool] = {}
_ASKING: dict[str, threading.Thread] = {}
_ACCEPTS_LOCK = threading.Lock()


def _server_key(client: Any) -> str:
    base = getattr(getattr(client, "settings", None), "base_url", None)
    return str(base) if base else f"client:{id(client)}"


def reset_feature_cache() -> None:
    """Forget every answer (tests that swap the server)."""
    with _ACCEPTS_LOCK:
        _ACCEPTS.clear()
        _ASKING.clear()


def server_accepts(client: Any, *, timeout: float = FEATURE_CHECK_SECONDS) -> bool:
    """Whether the server declares ``run_log_stream``, asked for at most
    ``timeout`` seconds: opening a run never waits longer on a live log. The
    answer -- a failure too, and a late one when it comes -- is kept for the
    process, so the check costs one run at most ``timeout`` and every later
    run nothing."""
    key = _server_key(client)
    with _ACCEPTS_LOCK:
        if key in _ACCEPTS:
            return _ACCEPTS[key]
        thread = _ASKING.get(key)
        wait = 0.0 if thread is not None else timeout
        if thread is None:

            def ask() -> None:
                try:
                    answer = bool(client.supports_feature(FEATURE))
                except Exception:  # noqa: BLE001 -- unknown means no
                    answer = False
                with _ACCEPTS_LOCK:
                    _ACCEPTS[key] = answer
                    _ASKING.pop(key, None)

            thread = threading.Thread(target=ask, name="probe-log-stream-check", daemon=True)
            _ASKING[key] = thread
            thread.start()
    thread.join(wait)
    with _ACCEPTS_LOCK:
        return _ACCEPTS.get(key, False)


def prepare(client: Any, log_path: str) -> bool:
    """Ask for a live stream of the output teed into ``log_path``: create the
    spool directory the helper looks for as it starts. False (and nothing on
    disk) when this process should not stream, or the server does not take it."""
    if client is None or not wanted_here():
        return False
    if not server_accepts(client):
        return False
    try:
        # Never an existing one: a spool left by a killed process holds ITS
        # cursor and segments, which this stream would take for its own.
        os.mkdir(live_dir(log_path), 0o700)
    except OSError:
        return False
    return True


# -- turning raw bytes into chunks -------------------------------------------------
def _forced_cut(buf: bytes, limit: int) -> tuple[int, int | None]:
    """``(cut, withhold_from)`` for a line too long to hold: after its last
    redraw, else after its last space or tab, else at ``limit`` moved back to
    a character boundary -- and there never inside a run of token-shaped bytes
    (`_TOKEN_RUN`, a credential's shape; the byte after ``buf`` is unknown, so
    a run reaching the end of it counts as crossing). Such a run is held back
    whole for the next chunk; one longer than ``MAX_TOKEN_RUN_BYTES`` is cut
    anyway, and ``withhold_from`` says where it starts: from there on it is
    withheld."""
    for sep in (b"\r", b" ", b"\t"):
        at = buf.rfind(sep, 0, limit)
        if at > 0:
            return at + 1, None
    cut = limit
    while 0 < cut < len(buf) and (buf[cut] & 0xC0) == 0x80:
        cut -= 1
    cut = cut or limit
    if cut < len(buf) and _TOKEN_RUN.match(buf, cut).end() == cut:
        return cut, None  # the next byte is no part of a token: nothing crosses
    start = cut - _TOKEN_RUN.match(buf[:cut][::-1]).end()
    if start == cut:
        return cut, None
    if cut - start <= MAX_TOKEN_RUN_BYTES:
        return start, None
    return cut, start


def _unterminated_pem(buf: bytes, end: int) -> int | None:
    """Start of the line holding the last private key BEGIN in ``buf[:end]``
    when no END follows it there, else None."""
    last = None
    for match in _PEM_BEGIN.finditer(buf, 0, end):
        last = match
    if last is None or _PEM_END.search(buf, last.end(), end):
        return None
    return buf.rfind(b"\n", 0, last.start()) + 1


@dataclass(frozen=True)
class Cut:
    """Where one chunk ends in the bytes read (`plan_cut`)."""

    #: Bytes at the front that ship now; 0 holds them all.
    size: int
    #: The chunk ends where a line (or the stream) ends. False after a forced
    #: cut: the next chunk continues the same line.
    at_line_end: bool = True
    #: A token-shaped run too long to hold crosses the cut: from here to
    #: ``size`` it is withheld, and so is its rest at the next chunk's start.
    withhold_from: int | None = None


def plan_cut(
    buf: bytes, *, final: bool, after_gap: bool = False, room: int = MAX_CHUNK_RAW_BYTES
) -> Cut:
    """Where the next chunk of ``buf`` ends.

    Complete lines only, up to ``MAX_CHUNK_RAW_BYTES`` and ``room`` (what is
    left of the pass's budget). ``final`` (the stream has ended and ``buf``
    runs to its end) ships a last line with no newline. A line too long to
    hold is cut (`_forced_cut`) only with a whole chunk's room: with less, the
    next pass has it. ``after_gap`` (``buf`` starts where output was dropped):
    held until enough follows to see whether it resumed inside a private key
    block (`render`).
    """
    if (
        after_gap
        and not final
        and len(buf) < MAX_PEM_HOLD_BYTES
        and _PEM_END.search(buf) is None
    ):
        return Cut(0)
    limit = min(len(buf), MAX_CHUNK_RAW_BYTES, room)
    newline = buf.rfind(b"\n", 0, limit)
    withhold = None
    if newline >= 0:
        end, whole = newline + 1, True
    elif final and len(buf) <= limit:
        end, whole = len(buf), True
    elif len(buf) > MAX_PARTIAL_LINE_BYTES and room >= MAX_CHUNK_RAW_BYTES:
        (end, withhold), whole = _forced_cut(buf, limit), False
    else:
        return Cut(0)
    held = _unterminated_pem(buf, end)
    if held is not None and not final and end - held <= MAX_PEM_HOLD_BYTES:
        return Cut(held)
    return Cut(end, whole, withhold)


def shippable(buf: bytes, *, final: bool, after_gap: bool = False) -> int:
    """How many bytes at the front of ``buf`` may ship now (`plan_cut`); 0
    holds them all."""
    return plan_cut(buf, final=final, after_gap=after_gap).size


def collapse_redraws(text: str) -> str:
    """Each line as a terminal left it: the last frame a ``\\r`` redraw drew.
    A text that ends in a redraw (a chunk cut at one) keeps that ``\\r``: the
    next chunk's first frame then replaces this one where the chunks are
    joined, instead of being appended to it."""
    lines = text.replace("\r\n", "\n").split("\n")
    for index, line in enumerate(lines):
        if "\r" in line:
            frames = [frame for frame in line.split("\r") if frame.strip()]
            redraw = "\r" if index == len(lines) - 1 and line.endswith("\r") else ""
            lines[index] = (frames[-1] if frames else "") + redraw
    return "\n".join(lines)


def render(raw: bytes, in_pem: bool, after_gap: bool = False) -> tuple[str, bool]:
    """``(text before redaction, in_pem after)`` for one chunk's raw bytes.

    ``in_pem`` says an earlier chunk withheld the start of a private key block
    that had not ended: its lines are dropped through the END line.
    ``after_gap`` says the chunk starts where output was dropped: an END line
    within ``MAX_PEM_HOLD_BYTES`` with no BEGIN before it means the gap took
    the block's BEGIN, and everything up to that END is key material."""
    lead = ""
    if after_gap and not in_pem:
        end = _PEM_END.search(raw, 0, MAX_PEM_HOLD_BYTES + 64)
        if end is not None and _PEM_BEGIN.search(raw, 0, end.start()) is None:
            in_pem, lead = True, _PEM_RESUMED
    if in_pem:
        end = _PEM_END.search(raw)
        if end is None:
            return "", True
        rest = raw.find(b"\n", end.end())
        raw = raw[rest + 1 :] if rest >= 0 else b""
        in_pem = False
    held = _unterminated_pem(raw, len(raw))
    tail = ""
    if held is not None:
        # Held back as long as allowed and still not ended: never ship it.
        raw, tail, in_pem = raw[:held], _PEM_WITHHELD, True
    text = raw.decode("utf-8", errors="replace").replace("\x00", "")
    return lead + collapse_redraws(text) + tail, in_pem


def redact(text: str, context: str = "") -> str:
    """The final log's redaction (`outputs.redact_log_text`), applied to one
    chunk; text it cannot clean is withheld, keeping the chunk's place.

    ``context``: the text just before this chunk on the same line (the chunk
    before a forced cut). The two are redacted together -- a key name before
    the cut and its value after it are one credential -- and what is returned
    starts where that result stops agreeing with the context's own
    redaction: normally exactly this chunk's text, cleaned, and at worst a
    few already-shown characters again, never an uncleaned one."""
    if not text:
        return text
    from .outputs import redact_log_text

    if context:
        data, _result = redact_log_text(context + text)
        if data is None:
            return _WITHHELD.format(n=len(text.encode("utf-8")))
        combined = data.decode("utf-8")
        alone, _result = redact_log_text(context)
        known = alone.decode("utf-8") if alone is not None else ""
        shared = len(os.path.commonprefix([combined, known]))
        marker = combined.rfind("<redacted", 0, shared)
        if marker >= 0 and combined.find(">", marker) >= shared:
            shared = marker  # never start inside a replacement marker
        return combined[shared:]
    data, _result = redact_log_text(text)
    if data is None:
        return _WITHHELD.format(n=len(text.encode("utf-8")))
    return data.decode("utf-8")


@dataclass(frozen=True)
class Chunk:
    offset: int
    raw_len: int
    text: str
    write_epoch: int | None
    #: The private-key state after this chunk, committed once it is sent.
    in_pem: bool
    #: Committed with it too: the chunk ended inside a withheld token run...
    in_run: bool = False
    #: ...or at a forced cut: the text (before redaction) the next chunk is
    #: redacted with ("" when it ended at a line end).
    seam: str = ""


class _Outcome(StrEnum):
    SENT = "sent"
    SKIPPED = "skipped"  # refused as malformed: step past it, never resend
    RETRY = "retry"
    STOP = "stop"
    REBUILD = "rebuild"  # the run's attempt moved on: build it again


# -- the shipper -------------------------------------------------------------------
class LogStreamer:
    """Ships one spool (one stream) to one run. :meth:`start` runs it on a
    daemon thread; :meth:`stop` makes a last, bounded pass and removes the
    spool. :meth:`ship` is one pass, for a caller that owns the loop.

    Never raises into the program. Everything it touches is its own spool and
    its own POSTs."""

    def __init__(
        self,
        client: Any,
        run_id: str,
        log_path: str,
        stream: str,
        *,
        interval: float | None = None,
        epoch: Callable[[], int | None] | None = None,
    ):
        self.client = client
        self.run_id = run_id
        self.dir = live_dir(log_path)
        self.stream = stream
        self.interval = interval if interval is not None else interval_seconds()
        self._epoch = epoch
        self.cursor = self._load_cursor()
        self._pending: Chunk | None = None
        self._in_pem = False
        self._in_run = False
        self._seam = ""
        #: A 429's ``retry_after``, honoured by the next backoff.
        self._retry_after = 0.0
        #: The next chunk starts where output was dropped (a spool overflow,
        #: a skip ahead, a resumed cursor): check it for a cut key block.
        self._after_gap = self.cursor > 0
        self._failures = 0
        self._next_try = 0.0
        self._disabled = False
        self._stop_by: float | None = None
        self._wake = threading.Event()
        self._thread: threading.Thread | None = None
        self._pass_lock = threading.Lock()
        #: Chunks the server accepted (stored or already had), for diagnostics.
        self.delivered = 0

    # -- lifecycle -----------------------------------------------------------
    def start(self) -> "LogStreamer":
        thread = threading.Thread(target=self._run, name="probe-log-stream", daemon=True)
        thread.start()
        self._thread = thread
        return self

    def _run(self) -> None:
        try:
            while self._stop_by is None:
                self._safe_ship(final=False)
                self._wake.wait(self._wait_seconds())
            self._safe_ship(final=True, deadline=self._stop_by)
        finally:
            self._remove_spool()

    def stop(self, budget: float = FINAL_FLUSH_SECONDS) -> None:
        """Ship the last lines within ``budget`` seconds (plus at most
        ``STOP_GRACE_SECONDS`` for a POST in flight), then remove the spool.
        Call it once the helper has ended the stream (the tee has stopped)."""
        self._stop_by = time.monotonic() + max(0.0, budget)
        self._wake.set()
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(max(0.0, budget) + STOP_GRACE_SECONDS)
        elif thread is None:
            self._safe_ship(final=True, deadline=self._stop_by)
        self._remove_spool()

    def _wait_seconds(self) -> float:
        if self._failures:
            return max(self.interval, self._next_try - time.monotonic())
        return self.interval

    def _remove_spool(self) -> None:
        shutil.rmtree(self.dir, ignore_errors=True)

    def _safe_ship(self, *, final: bool, deadline: float | None = None) -> None:
        try:
            self.ship(final=final, deadline=deadline)
        except Exception:  # noqa: BLE001 -- the live view never breaks a run
            pass

    # -- one pass ------------------------------------------------------------
    def ship(self, *, final: bool = False, deadline: float | None = None) -> int:
        """Send what is ready; returns how many chunks the server took.

        ``final``: the stream is ending. Waits (to ``deadline``) for the helper
        to say where it ended, then sends everything, a last line with no
        newline included."""
        with self._pass_lock:
            if self._disabled:
                return 0
            if not final and time.monotonic() < self._next_try:
                return 0
            if final:
                while read_eof(self.dir) is None and deadline is not None and time.monotonic() < deadline:
                    time.sleep(0.05)
            budget = FINAL_RAW_BYTES if final else PASS_RAW_BYTES
            if self._pending is None:
                self._skip_ahead(keep=budget, over=max(budget, MAX_BACKLOG_BYTES))
            took = shipped = 0
            while shipped < budget:
                if deadline is not None and time.monotonic() >= deadline:
                    break
                # No chunk takes the pass past its budget (`plan_cut`'s room).
                chunk = self._pending or self._next_chunk(final=final, room=budget - shipped)
                if chunk is None:
                    break
                self._pending = chunk
                outcome = self._send(chunk, deadline)
                if outcome in (_Outcome.SENT, _Outcome.SKIPPED):
                    self._pending = None
                    self._after_gap = False
                    self._failures = 0
                    self._next_try = 0.0
                    took += outcome is _Outcome.SENT
                    shipped += chunk.raw_len
                    self._drop_sent_segments()
                    continue
                if outcome is _Outcome.REBUILD:
                    self._pending = None
                    continue
                if outcome is _Outcome.STOP:
                    self._disabled = True
                    self._pending = None
                    break
                self._failures += 1
                delay = min(_BACKOFF_START * 2 ** (self._failures - 1), _BACKOFF_CAP)
                # A 429 says how long: never sooner than that.
                delay = max(delay, min(self._retry_after, _BACKOFF_CAP))
                self._retry_after = 0.0
                self._next_try = time.monotonic() + delay
                break
            self.delivered += took
            return took

    def _skip_ahead(self, *, keep: int, over: int) -> None:
        """More than ``over`` bytes unsent: jump to the newest ``keep`` bytes,
        at a line start. What is skipped is a gap the server marks."""
        segments = list_segments(self.dir)
        if not segments:
            return
        end = max(start + size for start, _path, size in segments)
        if end - self.cursor <= over:
            return
        target = end - keep
        start, data = self._read(target, MAX_PARTIAL_LINE_BYTES)
        newline = data.find(b"\n")
        self.cursor = start + newline + 1 if newline >= 0 else start
        self._gap()

    def _gap(self) -> None:
        """What follows was not the stream's next byte: no carried state."""
        self._in_pem = self._in_run = False
        self._seam = ""
        self._after_gap = True

    def _next_chunk(self, *, final: bool, room: int = MAX_CHUNK_RAW_BYTES) -> Chunk | None:
        eof = read_eof(self.dir)
        start, data = self._read(self.cursor, MAX_CHUNK_RAW_BYTES + MAX_PARTIAL_LINE_BYTES)
        if start > self.cursor:
            # The helper dropped output this never sent (its spool was full):
            # the jump in offsets is how the server learns of the gap.
            self.cursor = start
            self._gap()
        if not data:
            return None
        ended = final and eof is not None and start + len(data) >= eof
        cut = plan_cut(data, final=ended, after_gap=self._after_gap, room=room)
        if cut.size <= 0:
            return None
        raw = data[: cut.size]
        # The rest of a run the chunk before withheld, and a run too long to
        # hold that this chunk's cut crosses: neither ships (`_forced_cut`).
        lead = _TOKEN_RUN.match(raw).end() if self._in_run else 0
        keep = cut.size if cut.withhold_from is None else cut.withhold_from
        text, in_pem = render(raw[lead:keep] if lead < keep else b"", self._in_pem, self._after_gap)
        withheld = cut.withhold_from is not None
        seam = ""
        if not cut.at_line_end and not withheld:
            seam = (self._seam + text)[-SEAM_CONTEXT_CHARS:]
        cleaned = redact(text, self._seam)
        if withheld and not (self._in_run and cut.withhold_from == 0):
            cleaned += _RUN_WITHHELD  # once per run: its rest adds nothing
        epoch = self._epoch() if self._epoch is not None else None
        return Chunk(
            offset=start,
            raw_len=cut.size,
            text=cleaned,
            write_epoch=epoch,
            in_pem=in_pem,
            in_run=withheld,
            seam=seam,
        )

    def _commit(self, chunk: Chunk) -> None:
        """The carried state after ``chunk``, now that the server has it."""
        self._in_pem, self._in_run, self._seam = chunk.in_pem, chunk.in_run, chunk.seam

    def _read(self, cursor: int, max_bytes: int) -> tuple[int, bytes]:
        """``(offset of the first byte, bytes)`` from the spool at ``cursor``,
        contiguous, at most ``max_bytes``. The offset is past ``cursor`` when
        the segment that held it was dropped."""
        out = bytearray()
        start: int | None = None
        for seg_start, path, size in list_segments(self.dir):
            if seg_start + size <= cursor and seg_start < cursor:
                continue  # sent already; deleted once the next segment exists
            position = max(cursor, seg_start)
            if start is None:
                start = position
            elif position != start + len(out):
                break  # a hole the budget made: stop at it, the next pass jumps
            try:
                with open(path, "rb") as fh:
                    fh.seek(position - seg_start)
                    out += fh.read(max_bytes - len(out))
            except OSError:
                break
            if len(out) >= max_bytes:
                break
        return (cursor if start is None else start), bytes(out)

    def _send(self, chunk: Chunk, deadline: float | None) -> _Outcome:
        body: dict[str, Any] = {
            "stream": self.stream,
            "raw_offset": chunk.offset,
            "raw_len": chunk.raw_len,
            "text": chunk.text,
        }
        if chunk.write_epoch is not None:
            body["write_epoch"] = chunk.write_epoch
        from .transport import deadline_scope, without_patience

        # The transport retries a 429/5xx itself, waiting out a Retry-After of
        # up to 10 s each time: unbounded, one POST could hold a close or a
        # recovery ~40 s. The whole POST gets POST_TIMEOUT_SECONDS, and never
        # more than the pass's own deadline; no enclosing patience scope
        # (`probe.init()`'s) stretches it.
        post_by = time.monotonic() + POST_TIMEOUT_SECONDS
        if deadline is not None:
            post_by = min(post_by, max(deadline, time.monotonic() + 0.5))
        try:
            with without_patience(), deadline_scope(post_by):
                response = self.client.transport.request(
                    "POST",
                    f"/v1/runs/{self.run_id}/log-chunks",
                    json_body=body,
                    idempotent=True,
                    timeout=POST_TIMEOUT_SECONDS,
                )
        except errors.TransportError:
            return _Outcome.RETRY
        except errors.RosError as exc:
            return self._refused(chunk, exc)
        except Exception:  # noqa: BLE001 -- whatever else, try again later
            return _Outcome.RETRY
        end = chunk.offset + chunk.raw_len
        try:
            next_offset = int((response.json() or {}).get("next_offset", end))
        except (ValueError, TypeError, AttributeError):
            next_offset = end
        if next_offset == end:
            self._commit(chunk)
        elif next_offset > end:
            # The server already had more: follow it.
            self._in_pem = self._in_run = False
            self._seam = ""
        self.cursor = max(next_offset, 0)
        self._save_cursor()
        return _Outcome.SENT

    def _refused(self, chunk: Chunk, exc: errors.RosError) -> _Outcome:
        status = exc.status or 0
        detail = exc.detail if isinstance(exc.detail, dict) else {}
        if status == 409 and detail.get("code") == "stale_write_epoch":
            fresh = self._epoch() if self._epoch is not None else None
            # This process still believes the old attempt: a newer one took
            # the run over, so this one stops talking.
            return _Outcome.REBUILD if fresh is not None and fresh != chunk.write_epoch else _Outcome.STOP
        if status == 409 and detail.get("code") == "too_many_streams":
            return _Outcome.STOP  # the attempt has all the streams the server keeps
        if status in (403, 404, 410):
            return _Outcome.STOP  # the run is gone, trashed, or not ours to write
        if status in (400, 413, 422):
            # Malformed for this server: resending the same body cannot help.
            self.cursor = chunk.offset + chunk.raw_len
            self._commit(chunk)
            self._save_cursor()
            return _Outcome.SKIPPED
        if status == 429:
            # The header (`RosError.retry_after`), else the body (#2012 sends both).
            asked = exc.retry_after if exc.retry_after is not None else detail.get("retry_after")
            try:
                self._retry_after = max(0.0, float(asked or 0))
            except (TypeError, ValueError):
                self._retry_after = 0.0
        return _Outcome.RETRY

    # -- the spool -----------------------------------------------------------
    def _drop_sent_segments(self) -> None:
        """Delete every segment wholly before the cursor that has a successor
        (the last one may still be growing; `stop` removes the spool)."""
        segments = list_segments(self.dir)
        for (seg_start, path, size), following in zip(segments, segments[1:]):
            if following[0] <= self.cursor and seg_start + size <= self.cursor:
                try:
                    os.unlink(path)
                except OSError:
                    pass

    def _load_cursor(self) -> int:
        try:
            with open(os.path.join(self.dir, CURSOR_NAME), encoding="ascii") as fh:
                return max(0, int(fh.read().strip()))
        except (OSError, ValueError):
            return 0

    def _save_cursor(self) -> None:
        path = os.path.join(self.dir, CURSOR_NAME)
        try:
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="ascii") as fh:
                fh.write(str(self.cursor))
            os.replace(tmp, path)
        except OSError:
            pass


def _epoch_of(run: Any) -> int | None:
    epoch = getattr(run, "write_epoch", None)
    return int(epoch) if isinstance(epoch, int) and not isinstance(epoch, bool) and epoch >= 1 else None


def handle_epoch(run: Any) -> Callable[[], int | None]:
    """The write epoch of this run handle, read at each POST (a reopen can
    move it). Holds the handle weakly: a stream never keeps a Run alive."""
    import weakref

    ref = weakref.ref(run)

    def read() -> int | None:
        handle = ref()
        return None if handle is None else _epoch_of(handle)

    return read


def active_epoch(run_id: str) -> Callable[[], int | None]:
    """The write epoch of the ``probe.init()`` run with this id, read at each
    POST (a reopen can move it), or None when this process holds no such
    binding. The fallback when the capture was not handed its run's handle
    (`handle_epoch`)."""

    def read() -> int | None:
        try:
            from . import fluent

            run = fluent.active_run()
        except Exception:  # noqa: BLE001
            return None
        if run is None or str(getattr(run, "id", "")) != run_id:
            return None
        return _epoch_of(run)

    return read


def drain_spool(
    client: Any,
    run_id: str,
    log_path: str,
    log_name: str,
    *,
    budget: float,
    stream: str | None = None,
    write_epoch: int | None = None,
) -> int:
    """A dead process's spool, sent from where its cursor stopped (the
    recovery path), then removed. Returns the chunks the server took.

    ``stream`` and ``write_epoch`` are what the dead process recorded when its
    stream started: the chunks carry that attempt, so once a newer attempt
    has taken the run over the server refuses them (409) and nothing of the
    dead attempt lands in the new one's log. A record without an epoch (the
    process never learned it) sends none -- the server's current attempt."""
    if not os.path.isdir(live_dir(log_path)):
        return 0
    epoch = write_epoch if isinstance(write_epoch, int) and write_epoch >= 1 else None
    streamer = LogStreamer(
        client,
        run_id,
        log_path,
        stream or stream_for(log_name),
        epoch=(lambda: epoch) if epoch is not None else None,
    )
    try:
        if client is None:
            return 0
        return streamer.ship(final=True, deadline=time.monotonic() + max(0.0, budget))
    except Exception:  # noqa: BLE001 -- the final artifact is the durable copy
        return 0
    finally:
        streamer._remove_spool()
