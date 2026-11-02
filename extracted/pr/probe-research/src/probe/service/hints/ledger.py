"""the ledger of which records each hint carried, so the same record is not hinted twice; its receipt and sweep."""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import secrets
import time
from pathlib import Path

from ..watch.alertpoll import Endpoint
from probe.service.hints.delivery import (
    DeliveryState,
    LEDGER_TAIL_BYTES,
    delivery_facts,
    delivery_receipt,
    record_keys,
)
from probe.service.hints.state import Followed, Lookup, Skip, _State
from probe.service.hints.tail import HINTS_LIVE_BEAT_S, UNDELIVERABLE_PROBE_S, _safe
from probe.service.hints.triggers.window import shows_mid_turn
#: The most record doc ids a request names as shown already (`exclude_doc_ids`):
#: a long turn of window hints passes 50. A server that answered a window
#: lookup accepts 200; any other may be one before them (#3402), which refuses
#: more than LEGACY_EXCLUDE_DOC_IDS with a 422.
MAX_EXCLUDE_DOC_IDS = 100
#: Where each hint's records are kept (`<service dir>/hints/<sid>.jsonl`), and
#: for how long (`mailbox.KEEP_CLAIMED_S`: the claim log's own files).
LEDGER_DIR = "hints"
KEEP_LEDGER_S = 7 * 24 * 3600.0
#: Ledgers past KEEP_LEDGER_S are looked for at most this often.
SWEEP_EVERY_S = 24 * 3600.0


class LedgerMixin:
    """Part of HintLane: its methods run with `self` the HintLane; compose() folds them into HintLane."""

    def _deliver(self, job: Lookup, state: _State, hint: str, records: object) -> tuple[bool, str]:
        session = job.session
        keys = record_keys(records)
        with state.lock:
            if state.epoch != job.epoch:
                self.stats["stale"] += 1
                return False, Skip.STALE
            if job.happened < state.posted_happened:
                self.stats["superseded"] += 1
                return False, Skip.SUPERSEDED
            if keys and (
                keys <= self._seen(session, state)
                # A hint posted while this one was asked, and delivered since,
                # shares a record with it: asked after it, the server would have
                # left that record out. (One still waiting is replaced by this.)
                or (state.posted != job.posted_before and keys & self._delivered_records(session, state))
            ):
                self.stats["repeat"] += 1
                return False, Skip.REPEAT
            from probe.shared import mailbox

            message = {"id": "h" + secrets.token_hex(6), "session": job.sid, "kind": mailbox.Kind.MESSAGE.value,
                       "text": hint, "made_at": self.wall(), "origin": mailbox.ORIGIN_HINT}
            if not self._post(job.sid, session.state, message):
                self.stats["not_posted"] += 1
                return False, Skip.NOT_POSTED
            # Its slot holds one hint: an earlier one still waiting was replaced
            # (`mailbox.publish_here`), so it is no longer in the mailbox's files,
            # which are all `_seen` reads.
            if state.ledger is not None:
                state.ledger[message["id"]] = keys
            state.posted += 1
            state.posted_happened = max(state.posted_happened, job.happened)
            self._remember(job.sid, message["id"], keys)
        self.stats["posted"] += 1
        with contextlib.suppress(Exception):
            self._posted(job.sid)
        return True, "posted"

    def _shown(self, session: Followed, state: _State) -> list:
        """Each of the ledger's hints, newest first, as its record keys, that the
        session was delivered (the claim log, `claimed/`) or that waits in its
        mailbox now (R3), read from the mailbox's own files: a hint replaced in
        its slot, withdrawn, expired or removed by any other deliverer's rules
        never counts as shown. Under the session's lock."""
        if state.ledger is None:
            state.ledger = self._load_ledger(session.sid)
        ids: set = set()
        for read in (self._delivered, self._waiting):
            try:
                ids |= read(session.sid, session.state)
            except Exception:  # noqa: BLE001 -- unknown: none of these counts
                pass
        return [keys for mid, keys in reversed(state.ledger.items()) if mid in ids]

    def _seen(self, session: Followed, state: _State) -> set:
        """The records the session was shown or has waiting (`_shown`)."""
        return set().union(*self._shown(session, state))

    def _delivered_records(self, session: Followed, state: _State) -> set:
        """The records of the ledger's hints the session was delivered (the
        claim log), none waiting. Under the session's lock."""
        if state.ledger is None:
            state.ledger = self._load_ledger(session.sid)
        try:
            ids = self._delivered(session.sid, session.state)
        except Exception:  # noqa: BLE001 -- unknown: none counts
            return set()
        return set().union(*(keys for mid, keys in state.ledger.items() if mid in ids))

    # -- the ledger: which records each hint carried ------------------------------

    def _ledger_path(self, sid: str) -> Path:
        if self._ledger_dir is None:
            from ...foundation.service_api import paths

            self._ledger_dir = paths.service_dir() / LEDGER_DIR
        return self._ledger_dir / f"{_safe(sid)}.jsonl"

    def _load_ledger(self, sid: str) -> dict:
        path = self._ledger_path(sid)
        self._sweep(path.parent)
        out: dict = {}
        try:
            with path.open("rb") as handle:
                size = os.fstat(handle.fileno()).st_size
                handle.seek(max(0, size - LEDGER_TAIL_BYTES))
                text = handle.read().decode("utf-8", "replace")
        except OSError:
            return out
        for line in text.splitlines():
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            if isinstance(entry, dict) and isinstance(entry.get("id"), str) and isinstance(entry.get("keys"), list):
                out[entry["id"]] = frozenset(k for k in entry["keys"] if isinstance(k, str))
        return out

    def _remember(self, sid: str, message_id: str, keys: frozenset) -> None:
        path = self._ledger_path(sid)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600), "a", encoding="utf-8") as out:
                out.write(json.dumps({"id": message_id, "keys": sorted(keys), "at": self.wall()}) + "\n")
        except OSError as exc:
            self._log(f"hints: session {sid}: the ledger could not be written: {exc}")
        self._sweep(path.parent)

    def _ledger_events(self, sid: str, message_ids: list, event: str) -> None:
        """One ledger line per message id: what became of a hint posted here."""
        path = self._ledger_path(sid)
        at = self.wall()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600), "a", encoding="utf-8") as out:
                out.write("".join(json.dumps({"id": mid, "event": event, "at": at}) + "\n" for mid in message_ids))
        except OSError as exc:
            self._log(f"hints: session {sid}: the ledger could not be written: {exc}")

    def _receipt(self, session: Followed, state: _State, *, fresh: bool = False) -> dict | None:
        """The session's `delivery_receipt` (None when its files cannot be read),
        made again at most every HINTS_LIVE_BEAT_S unless `fresh`. A change into
        or out of UNDELIVERABLE is logged, and the receipt is left beside the
        session's hint marker for `probe doctor` (`mailbox.hints_delivery_path`)."""
        now = self.clock()
        with state.lock:
            if not fresh and state.delivery is not None and now - state.delivery_at < HINTS_LIVE_BEAT_S:
                return state.delivery
            calls, prompts = list(state.tool_calls), list(state.prompts)
            before = (state.delivery or {}).get("state")
        tail = self._tails.get(session.sid)
        try:
            facts = delivery_facts(session.sid, session.state, self._ledger_path(session.sid))
            receipt = delivery_receipt(facts, tool_calls=calls, prompts=prompts,
                                       mid_turn=tail is not None and shows_mid_turn(tail.adapter), now=self.wall())
        except Exception as exc:  # noqa: BLE001 -- unknown, never "fine" nor "broken"
            self._log(f"hints: session {session.sid}: delivery unknown: {type(exc).__name__}")
            return None
        with state.lock:
            state.delivery, state.delivery_at = receipt, now
        if receipt["state"] == DeliveryState.UNDELIVERABLE and before != DeliveryState.UNDELIVERABLE:
            self.stats["undeliverable"] += 1
            self._log(f"hints: session {session.sid}: its hints are not reaching the agent "
                      f"({receipt['missed']} missed, {receipt['unshown_since_shown']} not shown since the last "
                      f"one shown); its reader keeps its turns, and hints are asked only at a prompt, at most every "
                      f"{UNDELIVERABLE_PROBE_S / 60:.0f} min, until one is shown (quit the agent and resume the session)")
        elif before == DeliveryState.UNDELIVERABLE and receipt["state"] != DeliveryState.UNDELIVERABLE:
            self._log(f"hints: session {session.sid}: hints reach the agent again")
        with contextlib.suppress(Exception):
            from probe.shared import mailbox

            with mailbox.rooted(session.state):
                # `at` and `harness` for `probe doctor` only (`service_calls.hints_unreached`).
                mailbox.write_hints_delivery(session.sid, {**receipt, "at": self.wall(), "harness": session.harness})
        return receipt

    def _sweep(self, folder: Path) -> None:
        """Ledgers past KEEP_LEDGER_S go (their hints' claim files are gone
        too): at most every SWEEP_EVERY_S, so a service that runs for weeks
        does not keep every ended session's ledger."""
        if self._swept_at is not None and self.clock() - self._swept_at < SWEEP_EVERY_S:
            return
        self._swept_at = self.clock()
        now = time.time()
        with contextlib.suppress(OSError):
            for path in folder.glob("*.jsonl"):
                with contextlib.suppress(OSError):
                    if now - path.stat().st_mtime > KEEP_LEDGER_S:
                        path.unlink()


def exclude_doc_ids(shown: list, limit: int = MAX_EXCLUDE_DOC_IDS) -> list[str]:
    """The request's `exclude_doc_ids`: the doc ids of the records in `shown`
    (each hint's record keys, `<doc id> <date>`, newest hint first), each once,
    at most `limit`. A server that honors it leaves them out before it renders
    (a hint that repeats some records); one that does not ignores it, and
    `HintLane._deliver` still skips a hint whose records were all shown."""
    out: list[str] = []
    for keys in shown:
        for key in sorted(keys):
            doc = key.rsplit(" ", 1)[0]
            if doc and doc not in out:
                out.append(doc)
                if len(out) >= limit:
                    return out
    return out


def _window_scopes(ep: Endpoint | None) -> tuple:
    """A window lookup's own holds, beside `_scopes`: the server, without window
    lookups (a 404, a 422 naming `trigger`) or not answering; that key on that
    server, past its team's rate (a 429, `rate_limited`)."""
    if ep is None:
        return ()
    return (("window", ep.base_url), ("window_pair", ep.base_url, ep.key))


#: How the log names a hold's scope (never the key itself).
_SCOPE_NAMES = {"key": "this key", "server": "this server", "pair": "this key on this server",
                "window": "window lookups on this server", "window_pair": "window lookups of this key on this server"}


def _repeat_key(trigger: str, text: str) -> tuple[str, str]:
    return trigger, hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def _number(value: object) -> str:
    return f"{value:.3f}" if isinstance(value, (int, float)) and not isinstance(value, bool) else "-"
