"""queue one lookup per session and run them: who goes first, the rate bucket, the request, posting the hint."""

from __future__ import annotations

import contextlib
from probe.service.hints.delivery import LEDGER_WITHDRAWN
from probe.service.hints.ledger import (
    MAX_EXCLUDE_DOC_IDS,
    _SCOPE_NAMES,
    _number,
    _repeat_key,
    _window_scopes,
    exclude_doc_ids,
)
from probe.service.hints.request import names_trigger, scrubbed
from probe.service.hints.state import BUCKET_BURST, Followed, Lookup, Skip, WINDOW_MAX_SEGMENTS, _State
from probe.service.hints.tail import _scopes
from probe.service.hints.trigger import Trigger, _ASKED_FIRST
from probe.service.hints.triggers.window import (
    MAX_TEXT_CHARS,
    SCAN_MARGIN_CHARS,
    WINDOW_SEGMENT_CHARS,
    window_segments,
    window_text,
)
#: A window lookup takes a machine token only while at least this many are
#: left, so a prompt or a peer's message always finds one.
WINDOW_TOKEN_RESERVE = 2.0
#: The longest hint posted: one the server sends longer is dropped whole, never
#: cut mid-line into the agent's context (Probe renders ~170 chars a record).
MAX_HINT_CHARS = 4000
#: One request per session per this long; a newer trigger replaces a waiting one
#: (a search or a command never a prompt or a peer's message: _ASKED_FIRST).
SESSION_GAP_S = 10.0
#: The machine's token bucket.
BUCKET_PER_MIN = 20.0
#: A 429 holds that key on that server this long (as `alertpoll`, never the machine).
LIMITED_S = 60.0
#: `mode: off` (the team's setting): that key on that server is not asked again
#: for this long, from any session of this machine.
OFF_RECHECK_S = 10 * 60.0
#: The server refused the key (401 / 403): that key waits this long, on every server.
REFUSED_S = 5 * 60.0
#: A server without the route (404, a CLI ahead of its API): that server waits as long as `off`.
MISSING_S = OFF_RECHECK_S
LEGACY_EXCLUDE_DOC_IDS = 50
#: A session's last this-many request texts are never sent again (R16).
REPEATS = 32


class LookupsMixin:
    """Part of HintLane: its methods run with `self` the HintLane; compose() folds them into HintLane."""

    # -- triggers -----------------------------------------------------------------

    def trigger(self, session: Followed, trigger: str, text: str, senders: list | None = None,
                happened: float | None = None, newer: bool = True) -> bool:
        """A lookup asked for: queued (the latest per session, `_ASKED_FIRST` kept). A researcher
        prompt first withdraws the session's hint still waiting (R5; `newer`
        False: not one read on a first look). False when nothing was queued
        (an empty text queues nothing: a prompt that may not be looked up)."""
        text = (text or "").strip()[:MAX_TEXT_CHARS + SCAN_MARGIN_CHARS]  # `scrubbed` cuts it when sent
        state = self._state(session.sid)
        if trigger == Trigger.PROMPT:
            with state.lock:
                state.epoch += 1
                if newer:
                    self._take_back(session, state, "a newer prompt")
            with self._cv:
                # The window clock starts again (W1): the prompt gets its own
                # search now, and a window look waiting would ask about older work.
                state.window_since = happened if happened is not None else self.wall()
                state.window_messages.clear()
                waiting = self._pending.get(session.sid)
                if waiting is not None and waiting.trigger == Trigger.WINDOW:
                    del self._pending[session.sid]
        if not text:
            return False
        try:
            ep = self.endpoint_of(session.env)
        except Exception:  # noqa: BLE001 -- unknown: not asked
            ep = None
        if ep is None:
            self.stats["no_key"] += 1
            if not state.no_key_said:
                state.no_key_said = True
                self._log(f"hints: session {session.sid}: no Probe key in its CLI config (or its environment "
                          "names another endpoint or key); no hints")
            return False
        if not self._may_ask(state, trigger):
            return False
        now = self.clock()
        with self._cv:
            if now < self._off.get((ep.base_url, ep.key), float("-inf")):
                self.stats["quiet"] += 1
                return False
            if _repeat_key(trigger, text) in state.recent:
                self.stats["repeat_text"] += 1
                return False
            waiting = self._pending.get(session.sid)
            if waiting is not None and trigger not in _ASKED_FIRST and waiting.trigger in _ASKED_FIRST:
                # A prompt waiting out the gap is kept over the agent's search or
                # command: the researcher's ask is the better question.
                self.stats["outranked"] += 1
                return False
            self._pending.pop(session.sid, None)
            self._pending[session.sid] = Lookup(
                sid=session.sid, session=session, trigger=trigger, text=text, senders=list(senders or []),
                queued=now,
                happened=happened if happened is not None else self.wall(), epoch=state.epoch, ep=ep)
            self._evict()
            self.stats[f"trigger_{trigger}"] += 1
            self._cv.notify_all()
        return True

    def turn_ended(self, session: Followed, newer: bool = True) -> None:
        """The main agent's turn is over (TURN_END): a hint still waiting was for
        it, and the next prompt's hook would hand it over stale (R5), so it goes
        (`newer` False: not one read on a first look); a lookup in flight for it
        is stale, and one still waiting out the session's gap is not sent. The
        turn's window ends with it: its messages are not looked at again, and
        the clock starts again at the next turn's first step."""
        state = self._state(session.sid)
        with state.lock:
            state.epoch += 1
            if newer:
                self._take_back(session, state, "the turn ended")
        with self._cv:
            if self._pending.pop(session.sid, None) is not None:
                self.stats["ended"] += 1
            state.window_since = None
            state.window_messages.clear()

    def _take_back(self, session: Followed, state: _State, why: str) -> None:
        """A newer researcher prompt, or the end of the turn: the session's hints
        still waiting go (R5). Under the session's lock, so a lookup cannot post
        behind it."""
        try:
            gone = self._withdraw(session.sid, session.state)
        except Exception as exc:  # noqa: BLE001
            self._log(f"hints: session {session.sid}: could not withdraw a hint: {exc!r}")
            return
        if gone:
            self.stats["withdrawn"] += len(gone)
            self._ledger_events(session.sid, gone, LEDGER_WITHDRAWN)
            self._log(f"hints: session {session.sid}: {len(gone)} hint(s) withdrawn ({why})")
            with contextlib.suppress(Exception):
                self._posted(session.sid)

    # -- the lookups --------------------------------------------------------------

    def _lookup_loop(self, windows: bool) -> None:
        """One lookup thread: window lookups (`windows`), or every other kind
        (`take_due`)."""
        while True:
            with self._cv:
                job = None
                while not self._closed:
                    job, wait = self.take_due(windows)
                    if job is not None:
                        break
                    self._cv.wait(wait)
                if self._closed:
                    return
            try:
                self.lookup(job)
            except Exception as exc:  # noqa: BLE001 -- the thread outlives a bug; no hint
                self._log(f"hints: session {job.sid}: the lookup failed: {exc!r}")

    def _refill(self, now: float) -> None:
        rate = BUCKET_PER_MIN / 60.0
        self._tokens = min(BUCKET_BURST, self._tokens + max(0.0, now - self._filled_at) * rate)
        self._filled_at = now

    def take_due(self, windows: bool) -> tuple[Lookup | None, float | None]:
        """The next lookup of one kind that may go now, window lookups
        (`windows`) or every other kind, or `(None, how long to wait)` (None:
        until something is queued). A window leaves the machine's tokens to the
        other kind's lookups due now, and WINDOW_TOKEN_RESERVE besides. Call
        with the lane's condition held."""
        now = self.clock()
        for table in (self._holds, self._off):
            for scope in [k for k, until in table.items() if until <= now]:
                del table[scope]  # past: forgotten, so neither table grows
        if not self._pending:
            return None, None
        best, best_due, best_rank = None, None, None
        others_due_now = 0  # the other kind's lookups due now (a window leaves them their tokens)
        for sid, job in list(self._pending.items()):
            state = self._state(sid)
            if job.ep is not None and (job.ep.base_url, job.ep.key) in self._off:
                del self._pending[sid]  # its team's setting is off: not asked
                continue
            window = job.trigger == Trigger.WINDOW
            if window and not state.window_messages:
                del self._pending[sid]  # a prompt started the window again: nothing to look at
                continue
            scopes = (*_scopes(job.ep), *_window_scopes(job.ep)) if window else _scopes(job.ep)
            held = max((self._holds.get(scope, float("-inf")) for scope in scopes), default=float("-inf"))
            sent = state.window_last_sent if window else state.last_sent
            due = max(job.queued, sent + SESSION_GAP_S, held)
            if window != windows:  # the other thread's
                others_due_now += due <= now
                continue
            rank = (max(due, now), due)
            if best_rank is None or rank < best_rank:
                best, best_due, best_rank = job, due, rank
        if best is None:
            return None, None
        if best_due > now:
            return None, best_due - now
        self._refill(now)
        # A window never takes the machine's last tokens, nor those the other
        # thread's lookups due now need: a prompt finds one.
        need = WINDOW_TOKEN_RESERVE + others_due_now if windows else 1.0
        if self._tokens < need:
            return None, (need - self._tokens) / (BUCKET_PER_MIN / 60.0)
        self._tokens -= 1.0
        del self._pending[best.sid]
        state = self._state(best.sid)
        if best.trigger == Trigger.WINDOW:
            state.window_last_sent = now
            # Its messages, taken now; the clock starts again at the newest step.
            best.segments = window_segments(state.window_messages)
            state.window_messages.clear()
            state.window_since = state.window_seen
        else:
            state.last_sent = now
        return best, None

    def run_due(self) -> int:
        """Every lookup due now, on this thread, taken as the two lookup
        threads take them (the other kinds first, then the windows; tests).
        How many ran."""
        ran = 0
        while True:
            with self._cv:
                job, _wait = self.take_due(False)
                if job is None:
                    job, _wait = self.take_due(True)
            if job is None:
                return ran
            self.lookup(job)
            ran += 1

    def lookup(self, job: Lookup) -> None:
        """Ask the server about one trigger; post the hint when it fires. Fails
        open: any error is one log line and no hint."""
        session, state = job.session, self._state(job.sid)
        ep = job.ep
        if ep is None:
            return  # `trigger` queues none without one
        try:
            from probe.shared.harness import lookup as adapters

            harness = adapters.for_source(session.harness).name
        except Exception:  # noqa: BLE001
            harness = session.harness
        window = job.trigger == Trigger.WINDOW
        segments: list[str] = []
        try:
            if window:
                # Each message scanned before its cut, then joined clean.
                segments = [clean for clean in (scrubbed(m, WINDOW_SEGMENT_CHARS).strip() for m in job.segments)
                            if clean]
                text = window_text(segments)
            else:
                text = scrubbed(job.text)
        except Exception as exc:  # noqa: BLE001 -- unscanned text never leaves: no request
            self.stats["unscanned"] += 1
            self._log(f"hints: session {job.sid}: the secret scan failed ({type(exc).__name__}); not asked")
            return
        if window and not segments:
            return
        exclude: list = []
        for sender in job.senders:
            sid = self.senders.resolve(sender, session.env)
            if sid and sid != job.sid and sid not in exclude:
                exclude.append(sid)
        try:
            with state.lock:
                job.posted_before = state.posted
                shown = self._shown(session, state)
        except Exception:  # noqa: BLE001 -- unknown: none named (the all-repeated rule still holds)
            shown = []
        with self._cv:
            newer_server = any(pair[0] == ep.base_url for pair in self._window_ok)
        limit = MAX_EXCLUDE_DOC_IDS if newer_server else LEGACY_EXCLUDE_DOC_IDS
        body = {"text": text, "trigger": job.trigger, "session_id": job.sid,
                "exclude_session_ids": exclude, "exclude_doc_ids": exclude_doc_ids(shown, limit),
                "client": {"harness": harness, "mode": session.mode, "cli": self.version},
                "delivery": self._receipt(session, state, fresh=True)}
        if window:
            body["segments"] = segments
            if state.epoch != job.epoch:
                # Its turn ended, or a newer prompt came: the hint would be
                # dropped (`_deliver`), so it is not asked. Best effort: a turn
                # end read after this still drops it there.
                self.stats["stale"] += 1
                return
        started = self.clock()
        try:
            status, data = (self.window_transport if window else self.transport)(ep, body)
        except Exception as exc:  # noqa: BLE001 -- fail open
            status, data = None, None
            self._log(f"hints: session {job.sid}: the request failed: {type(exc).__name__}")
        took = (self.clock() - started) * 1000.0
        # Plan hints-latency R9: every answer's delay from the trigger, posted or
        # not, so a slow lookup shows even when it fires nothing.
        answered = f"answered {(self.wall() - job.happened) * 1000:.0f} ms after the trigger"
        line = f"hints: session {job.sid} {job.trigger}" + (f" ({len(segments)} messages)" if window else "")
        unsupported = self._window_answered(job, state, status, data) if window else False
        if status is None:
            self.stats["unanswered"] += 1
            held = ""
            if window:
                # A window waits WINDOW_TIMEOUT_S on its thread: while the server
                # is not answering, none goes for LIMITED_S.
                scope = _window_scopes(ep)[0]
                with self._cv:
                    self._holds[scope] = max(self._holds.get(scope, float("-inf")), self.clock() + LIMITED_S)
                self.stats["held_window_unanswered"] += 1
                held = f"; {_SCOPE_NAMES[scope[0]]} are not asked for {LIMITED_S:.0f} s"
            self._log(f"{line}: no answer in {took:.0f} ms; no hint{held}")
            return
        if window and (unsupported or status == 429 or (status == 200 and isinstance(data, dict)
                                                        and data.get("reason") == "rate_limited")):
            # A window's own: an older server without window lookups, or one
            # costing more than the team's rate has left. Prompts still ask.
            wait = MISSING_S if unsupported else LIMITED_S
            scope = _window_scopes(ep)[0 if unsupported else 1]
            with self._cv:
                self._holds[scope] = max(self._holds.get(scope, float("-inf")), self.clock() + wait)
            self.stats[f"held_window_{status}"] += 1
            self._log(f"{line}: answered {status}; {_SCOPE_NAMES[scope[0]]} are not asked for {wait:.0f} s; "
                      f"{answered}")
            return
        if status in (401, 403, 404, 429) or (status == 200 and isinstance(data, dict)
                                               and data.get("reason") == "rate_limited"):
            wait = {401: REFUSED_S, 403: REFUSED_S, 404: MISSING_S}.get(status, LIMITED_S)
            scope = _scopes(ep)[{401: 0, 403: 0, 404: 1}.get(status, 2)]
            with self._cv:
                self._holds[scope] = max(self._holds.get(scope, float("-inf")), self.clock() + wait)
            self.stats[f"held_{status}"] += 1
            self._log(f"{line}: answered {status}; {_SCOPE_NAMES[scope[0]]} is not asked for {wait:.0f} s; "
                      f"{answered}")
            return
        if status != 200 or not isinstance(data, dict):
            self.stats["refused"] += 1
            self._log(f"{line}: answered {status} in {took:.0f} ms; no hint; {answered}")
            return
        with self._cv:
            if not window:
                state.recent[_repeat_key(job.trigger, job.text)] = None
            while len(state.recent) > REPEATS:
                state.recent.popitem(last=False)
            mode = data.get("mode")
            if mode == "off":
                # The team's setting, for every session of this key on this server.
                self._off[(ep.base_url, ep.key)] = self.clock() + OFF_RECHECK_S
        fire = data.get("fire") is True
        hint = data.get("hint")
        outcome = "not shown"
        with self._cv:
            off = self.clock() < self._off.get((ep.base_url, ep.key), float("-inf"))
        if fire and mode == "on" and isinstance(hint, str) and hint.strip():
            if self._closed:
                outcome = Skip.CLOSED
            elif off:
                # Another lookup's answer turned the team's hints off meanwhile.
                self.stats["off"] += 1
                outcome = Skip.OFF
            elif len(hint) > MAX_HINT_CHARS:
                self.stats["too_long"] += 1
                outcome = Skip.TOO_LONG
            else:
                # Posted exactly as Probe rendered it: the mailbox shows a hint as-is
                # only when it starts with `[Probe] ` (its framing), so nothing is added.
                posted, why = self._deliver(job, state, hint, data.get("records"))
                outcome = f"posted {(self.wall() - job.happened) * 1000:.0f} ms after the trigger" if posted else why
        self.stats[f"mode_{mode}"] += 1
        self._log(f"{line}: mode={mode} fire={fire} reason={data.get('reason')} "
                  f"top={_number(data.get('top_score'))} in {took:.0f} ms; {outcome}; {answered}")

    def _window_answered(self, job: Lookup, state: _State, status: int | None, data: object) -> bool:
        """What a window lookup's answer proves (W3, `_window_works`): a 200 as a
        window shows the server and key do window lookups; a 404, or a 422
        naming `trigger`, that the server does not (True: `unsupported`). No
        answer, any other status, `engine_error` or `rate_limited` is one more
        failure in a row, the session's and its key's; a failure a retry can
        pass (no answer, a 5xx, a 429, `engine_error`, `rate_limited`) puts its
        messages back for the next look, unless its turn is over (a 4xx is
        about those messages: they go). A 200 that searched ends both runs."""
        ep = job.ep
        pair = (ep.base_url, ep.key)
        answer = data if status == 200 and isinstance(data, dict) else None
        unsupported = status == 404 or (status == 422 and names_trigger(data))
        with self._cv:
            if unsupported:
                for known in [p for p in self._window_ok if p[0] == ep.base_url]:
                    del self._window_ok[known]
            if answer is not None and answer.get("trigger_class") == Trigger.WINDOW:
                self._window_ok[pair] = True
            if answer is not None and answer.get("reason") not in ("engine_error", "rate_limited"):
                state.window_failures = 0
                self._window_key_failures.pop(pair, None)
                return False
            state.window_failures += 1
            self._window_key_failures[pair] = self._window_key_failures.get(pair, 0) + 1
            retry = status is None or status >= 500 or status == 429 or answer is not None
            if retry and state.epoch == job.epoch:
                # Looked at by no one: back as the oldest of the next look's messages.
                kept = [*reversed(job.segments), *state.window_messages][-WINDOW_MAX_SEGMENTS:]
                state.window_messages.clear()
                state.window_messages.extend(kept)
        return unsupported
