"""Session upload protocol 3: each retained event also goes up as an ATIF fragment.

The contract is `~/plans/research-os-atif-upload/CONTRACT.md` (§1-3, §7) and
prbe-knowledge `kb/session_receipts.py` (the door). `DoorWire` below answers as
that door does behind the research-os gateway: receipts carry `accepts`, a new
stream is pinned to the protocol of its first batch, protocol 3 needs
`fragment_version` on every batch and one fragment per event ordinal (the
fragment's `line.line_no`), and an open protocol-3 stream stays accepted after
protocol 3 stops being offered. With protocol 2 retired for new streams
(`SESSION_PROTOCOL2_NEW_STREAMS=false`, engine `protocol2_retired`) the door
refuses a new stream's protocol-2 batch 0 with 409 `protocol 2 retired` and the
receipts answer stops offering 2, only while protocol 3 can replace it.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sqlite3
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

from probe.cli import backfill_transcripts as bt
from probe.tap_core import atif_fragment
from probe.tap_core import session_journal as sj
from probe.tap_core.session_journal import (
    DeliveryPending,
    Journal,
    ReconciliationRequired,
    canonical_payload,
)
from test_backfill_transcripts_upload import _transcript

_AGENT = Path(__file__).resolve().parent.parent
GOLDENS = _AGENT / "tests" / "fixtures" / "probe_events"
HARNESSES = ("claude_code", "codex", "pi", "kimi_code")
CUSTOMER = "synthetic"
CWD = "/synthetic"
GITHUB = "ghp_" + hashlib.sha256(b"synthetic-protocol-3-split").hexdigest()[:36]

#: prbe-knowledge `kb/session_receipts.py` `_FIELDS` (#630): the keys the door
#: digests. A key one side digests and the other does not breaks every receipt.
DOOR_FIELDS = {
    "session_id", "batch_seq", "cwd", "events", "fragments", "fragment_version", "finalize",
    "protocol_version", "stream_id", "source_byte_start", "source_byte_end",
    "source_line_start", "source_line_end", "event_start", "event_end", "prefix_sha256",
    "provenance", "snapshot_byte_end", "snapshot_sha256",
}


class DoorWire:
    """The engine's receipts door behind the gateway, for one customer."""

    base_url = "http://synthetic.invalid"
    timeout = 1
    token = "synthetic"

    def __init__(self, source="claude_code", *, offers=True, events=False, versions=(1,)):
        self.source = source
        #: What the receipts answer advertises (`accepts`); None: an old server.
        self.offers: bool | None = offers
        #: Whether the door takes a NEW protocol-3 stream (the customer list).
        #: Normally the same as `offers`; they differ during a settings rollout.
        self.enabled = bool(offers)
        self.events = events
        self.versions = list(versions)
        self.streams: dict[str, dict] = {}
        self.receipts_rows: dict[tuple[str, int], dict] = {}
        self.accepted: dict[tuple[str, int], bytes] = {}
        self.calls: list[bytes] = []
        #: A 409 detail the door gives every protocol-3 batch 0 (refusal tests).
        self.refuse_batch0: str | None = None
        #: SESSION_PROTOCOL2_NEW_STREAMS: False retires protocol 2 for NEW streams.
        self.protocol2_new_streams = True

    def _protocol2_retired(self, protocol3: bool) -> bool:
        """The engine's `protocol2_retired`: only while protocol 3 can take its
        place (offered or enabled, and a fragment version the door reads)."""
        return not self.protocol2_new_streams and protocol3 and bool(self.versions)

    def offer(self, offers: bool) -> None:
        self.offers = self.enabled = offers

    def receipts(self, sid, *, after=-1, limit=None):
        stream = self.streams.get(sid)
        result = {
            "protocol_version": stream["protocol_version"] if stream else 2,
            "customer_id": CUSTOMER,
            "source": self.source,
            "session_id": sid,
            "state": "ready" if stream else "absent",
            "receipts": [],
        }
        if self.offers is not None:
            result["accepts"] = {
                "protocols": ([] if self._protocol2_retired(bool(self.offers)) else [2])
                + ([3] if self.offers else []),
                "fragment_versions": list(self.versions),
                "events": self.events,
            }
        if stream:
            result["stream"] = {k: v for k, v in stream.items() if k != "protocol_version"}
            rows = [r for (s, seq), r in sorted(self.receipts_rows.items()) if s == sid and seq > after]
            result["receipts"] = rows[:limit] if limit is not None else rows
        return copy.deepcopy(result)

    @staticmethod
    def invalid(body: dict) -> str | None:
        """Gateway + door validation of the batch envelope."""
        protocol = body.get("protocol_version")
        start, end = body["event_start"], body["event_end"]
        if protocol == 2:
            if "fragments" in body or "fragment_version" in body:
                return "fragments belong to protocol 3"
            events = body.get("events", [])
        elif protocol == 3 and type(protocol) is int:
            if type(body.get("fragment_version")) is not int:
                return "fragment_version belongs to protocol 3, and protocol 3 requires it"
            if body.get("finalize"):
                if body.get("fragments") or body.get("events"):
                    return "finalize cannot carry fragments"
                return None
            fragments = body.get("fragments")
            if not isinstance(fragments, list) or len(fragments) != end - start:
                return "fragment coverage does not match payload"
            ordinals = [
                f.get("line", {}).get("line_no") if isinstance(f, dict) else None for f in fragments
            ]
            if ordinals != list(range(start, end)):
                return "fragment ordinals are not contiguous"
            if "events" not in body:
                return None
            events = body["events"]
        else:
            return "unsupported codec"
        if body.get("finalize") and events:
            return "finalize cannot carry events"
        if [e.get("line_no") for e in events] != list(range(start, end)):
            return "retained-event ordinals are not contiguous"
        return None

    def post(self, encoded: bytes):
        self.calls.append(encoded)
        body = json.loads(encoded)
        problem = self.invalid(body)
        if problem:
            return 422, {"detail": f"invalid transcript protocol: {problem}"}
        sid, seq, protocol = body["session_id"], body["batch_seq"], body["protocol_version"]
        digest = hashlib.sha256(canonical_payload(body)).hexdigest()
        if protocol == 3 and seq == 0 and self.refuse_batch0:
            return 409, {"detail": self.refuse_batch0}
        stream = self.streams.get(sid)
        if stream is None:
            if seq != 0:
                return 409, {"detail": "unknown stream; first sequence must be zero"}
            if protocol == 3 and not self.enabled:
                return 409, {"detail": "protocol 3 not enabled"}
            if protocol == 2 and self._protocol2_retired(self.enabled):
                return 409, {"detail": "protocol 2 retired"}
            stream = {
                "stream_id": body["stream_id"], "protocol_version": protocol, "last_seq": -1,
                "source_byte_end": 0, "source_line_end": 0, "event_end": 0,
                "prefix_sha256": sj.EMPTY_HASH, "finalized": False,
            }
        if stream["stream_id"] != body["stream_id"]:
            return 409, {"detail": "session owned by another stream; reconcile receipts first"}
        if stream["protocol_version"] != protocol:
            return 409, {"detail": "protocol mismatch"}
        if (sid, seq) in self.receipts_rows:
            if self.receipts_rows[(sid, seq)]["body_sha256"] != digest:
                return 409, {"detail": "batch identity already accepted with different content"}
            return 202, {"status": "duplicate", "protocol_version": protocol,
                         "receipt": self.receipts_rows[(sid, seq)]}
        if seq != stream["last_seq"] + 1 or any(
            body[f"{unit}_start"] != stream[f"{unit}_end"]
            for unit in ("source_byte", "source_line", "event")
        ):
            return 409, {"detail": "batch does not continue the acknowledged source/event cursor"}
        receipt = {k: body[k] for k in (
            "batch_seq", "source_byte_end", "source_line_end", "event_end", "prefix_sha256",
        )}
        receipt.update(body_sha256=digest, finalized=bool(body.get("finalize")))
        self.receipts_rows[(sid, seq)] = receipt
        self.accepted[(sid, seq)] = encoded
        stream.update(
            last_seq=seq, source_byte_end=body["source_byte_end"],
            source_line_end=body["source_line_end"], event_end=body["event_end"],
            prefix_sha256=body["prefix_sha256"], finalized=bool(body.get("finalize")),
        )
        self.streams[sid] = stream
        return 202, {"status": "accepted", "protocol_version": protocol, "receipt": receipt}

    def bodies(self, sid) -> list[dict]:
        return [json.loads(b) for (s, _), b in sorted(self.accepted.items()) if s == sid]


# -- helpers ------------------------------------------------------------------------


def _write(path: Path, lines: list[dict]) -> Path:
    with path.open("ab") as handle:
        for line in lines:
            handle.write(json.dumps(line).encode() + b"\n")
    return path


def _user(sid: str, text, n: int = 0) -> dict:
    return {
        "type": "user", "sessionId": sid, "cwd": CWD, "uuid": f"u-{n}",
        "timestamp": "2026-10-05T10:01:00.000Z",
        "message": {"role": "user", "content": text},
    }


def _assistant(sid: str, text: str, n: int = 0) -> dict:
    return {
        "type": "assistant", "sessionId": sid, "cwd": CWD, "uuid": f"a-{n}",
        "timestamp": "2026-10-05T10:01:01.000Z",
        "message": {"role": "assistant", "model": "synthetic-model", "id": f"msg-{n}",
                    "content": [{"type": "text", "text": text}]},
    }


def _session(tmp_path: Path, lines: list[dict] | None = None, name="s") -> tuple[str, Path]:
    sid = str(uuid.uuid4())
    path = tmp_path / f"{name}-{sid}.jsonl"
    path.write_bytes(b"")
    if lines is None:
        lines = [_user(sid, f"turn {i}", i) for i in range(6)]
    _write(path, lines)
    return sid, path


def _journal(tmp_path: Path, wire: DoorWire, name="state") -> Journal:
    return Journal(wire.base_url, CUSTOMER, wire.source, directory=tmp_path / name)


def _drain(journal: Journal, wire, sid: str, **stage) -> list[bytes]:
    sent = []
    while (body := journal.stage(sid, cwd=CWD, **stage)) is not None:
        journal.deliver(sid, wire)
        sent.append(body)
    return sent


def _start(journal: Journal, wire, sid: str, path: Path, *, historical=False) -> dict:
    return journal.ensure(sid, path, wire.receipts(sid), historical=historical, cwd=CWD)


def _flatten(outputs) -> list[dict]:
    events = []
    for out in outputs:
        for raw in out if isinstance(out, list) else [] if out is None else [out]:
            events.append({"line_no": len(events), "raw": raw})
    return events


def _expected_fragments(events: list[dict]) -> list[dict]:
    """The contract's order, by hand: events scrubbed together, fragment each,
    fragments scrubbed to their own fixed point."""
    scrubbed = sj._scrub_content({"events": events})["events"]
    return sj._scrub_content({"fragments": [atif_fragment.fragment(e) for e in scrubbed]})["fragments"]


def _tables(journal: Journal) -> dict[str, set[str]]:
    with sqlite3.connect(journal.db_path) as conn:
        return {
            table: {row[0] for row in conn.execute(f"SELECT session_id FROM {table}")}
            for table in ("sessions", "fragment_sessions")
        }


# -- the wire contract ---------------------------------------------------------------


def test_the_digested_fields_are_the_doors():
    assert set(sj._FIELDS) == DOOR_FIELDS
    assert len(sj._FIELDS) == len(DOOR_FIELDS)


def test_fragment_refusals_are_one_constant():
    assert sj.PROTOCOL3_REFUSALS == ("protocol 3 not enabled", "protocol mismatch")


# -- negotiation (§1) ---------------------------------------------------------------


def _answer(**accepts):
    return {"protocol_version": 2, "state": "absent", "accepts": accepts} if accepts else {
        "protocol_version": 2, "state": "absent"}


@pytest.mark.parametrize(
    "remote,expected",
    [
        pytest.param(_answer(), (2, False), id="no-accepts-old-server"),
        pytest.param(_answer(protocols=[2], fragment_versions=[1], events=True), (2, False),
                     id="protocol-2-only"),
        pytest.param(_answer(protocols=[2, 3], fragment_versions=[1], events=False), (3, False),
                     id="offered"),
        pytest.param(_answer(protocols=[2, 3], fragment_versions=[1], events=True), (3, True),
                     id="offered-with-events"),
        pytest.param(_answer(protocols=[2, 3], fragment_versions=[2], events=True), (2, False),
                     id="fragment-version-unsupported"),
        pytest.param(_answer(protocols=[2, 3], events=False), (2, False), id="no-versions"),
        pytest.param(_answer(protocols=[2, "3", True], fragment_versions=[1]), (2, False),
                     id="only-the-integer-3"),
        pytest.param(_answer(protocols=[2, 3], fragment_versions=[1.0, True]), (2, False),
                     id="only-an-integer-version"),
    ],
)
def test_negotiate(remote, expected):
    assert sj.negotiate(remote) == expected


def test_negotiate_reads_the_offer_before_importing_the_builder(monkeypatch):
    monkeypatch.setattr(sj, "_fragment_module", lambda: pytest.fail("imported the builder"))
    assert sj.negotiate(_answer()) == (2, False)
    assert sj.negotiate(_answer(protocols=[2], fragment_versions=[1], events=True)) == (2, False)
    assert sj.negotiate(_answer(protocols=[2, 3], events=True)) == (2, False)


def test_negotiate_needs_the_builder(monkeypatch):
    monkeypatch.setattr(sj, "_fragment_module", lambda: None)
    assert sj.negotiate(_answer(protocols=[2, 3], fragment_versions=[1], events=True)) == (2, False)


def test_session_journal_imports_without_the_fragment_builder():
    """Protocol 2 never depends on the vendored engine code: importing the
    journal does not import it, and a builder that fails to import leaves
    every new stream on protocol 2."""
    script = (
        "import importlib.abc, sys\n"
        "class Broken(importlib.abc.MetaPathFinder):\n"
        "    def find_spec(self, name, path=None, target=None):\n"
        "        if name.endswith('.atif_fragment'):\n"
        "            raise ImportError('synthetic: the vendored builder does not import')\n"
        "sys.meta_path.insert(0, Broken())\n"
        "from probe.tap_core import session_journal as sj\n"
        "assert 'probe.tap_core.atif_fragment' not in sys.modules\n"
        "offer = {'state': 'absent', 'accepts': {'protocols': [2, 3], 'fragment_versions': [1]}}\n"
        "print(sj.negotiate(offer))\n"
    )
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "(2, False)"


@pytest.mark.parametrize("offers", [None, False, True])
def test_a_new_stream_starts_on_what_is_offered(tmp_path, offers):
    wire = DoorWire(offers=offers)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    (body,) = wire.bodies(sid)
    expected = 3 if offers else 2
    assert body["protocol_version"] == expected
    assert ("fragments" in body) is (expected == 3) and ("events" in body) is (expected == 2)
    state = journal.get(sid)
    assert state["protocol_version"] == expected  # recorded once the server holds it
    journal.close()


def test_the_protocol_is_recorded_only_once_the_server_holds_the_stream(tmp_path):
    wire = DoorWire(offers=True)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    state = journal.get(sid)
    assert state["protocol_offer"] == 3 and "protocol_version" not in state
    assert journal.stage(sid, cwd=CWD) is not None
    assert "protocol_version" not in journal.get(sid)  # staged is not accepted
    journal.deliver(sid, wire)
    assert journal.get(sid)["protocol_version"] == 3
    journal.close()


def test_a_protocol_2_stream_stays_on_2_when_3_is_offered_later(tmp_path):
    wire = DoorWire(offers=False)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    wire.offer(True)
    _write(path, [_user(sid, "after the offer", 9)])
    _drain(journal, wire, sid)
    assert [b["protocol_version"] for b in wire.bodies(sid)] == [2, 2]
    # A journal that lost its state adopts the stream the server holds, on 2.
    fresh = _journal(tmp_path, wire, name="other-device")
    _write(path, [_user(sid, "on another device", 10)])
    _start(fresh, wire, sid, path)
    assert fresh.get(sid)["protocol_version"] == 2
    _drain(fresh, wire, sid)
    assert [b["protocol_version"] for b in wire.bodies(sid)] == [2, 2, 2]
    journal.close()
    fresh.close()


def test_a_protocol_3_stream_stays_on_3_when_the_offer_is_withdrawn(tmp_path):
    wire = DoorWire(offers=True)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    wire.offer(False)  # the kill switch: no NEW protocol-3 stream
    _write(path, [_user(sid, "after the withdrawal", 9)])
    _drain(journal, wire, sid)
    journal.close()
    # A restarted tap keeps it (the journal recorded it), and so does a fresh
    # journal adopting the server's stream.
    reopened = _journal(tmp_path, wire)
    _write(path, [_user(sid, "after a restart", 10)])
    _drain(reopened, wire, sid)
    fresh = _journal(tmp_path, wire, name="other-device")
    _write(path, [_user(sid, "on another device", 11)])
    _start(fresh, wire, sid, path)
    _drain(fresh, wire, sid)
    assert [b["protocol_version"] for b in wire.bodies(sid)] == [3, 3, 3, 3]
    assert all(b["fragment_version"] == atif_fragment.FRAGMENT_VERSION for b in wire.bodies(sid))
    reopened.close()
    fresh.close()


# -- restart on protocol 2 when the door will not take protocol 3 at batch 0 ---------


@pytest.mark.parametrize("detail", sj.PROTOCOL3_REFUSALS)
def test_a_refused_protocol_3_batch_0_restarts_the_stream_on_2(tmp_path, detail):
    wire = DoorWire(offers=True)
    wire.refuse_batch0 = detail
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    staged = journal.stage(sid, cwd=CWD)
    assert json.loads(staged)["protocol_version"] == 3
    assert _tables(journal) == {"sessions": {sid}, "fragment_sessions": set()}  # offered only
    with pytest.raises(DeliveryPending) as refused:
        journal.deliver(sid, wire)
    assert refused.value.retryable
    assert journal.pending(sid) is None
    state = journal.get(sid)
    assert state["protocol_offer"] == 2 and state["send_events"] is False
    assert state["source_byte_end"] == 0 and state["last_seq"] == -1
    assert _tables(journal) == {"sessions": {sid}, "fragment_sessions": set()}
    _drain(journal, wire, sid)
    (body,) = wire.bodies(sid)
    assert body["protocol_version"] == 2 and body["batch_seq"] == 0
    assert body["source_byte_start"] == 0 and body["source_byte_end"] == path.stat().st_size
    assert journal.get(sid)["protocol_version"] == 2
    journal.close()


def test_a_rollout_race_withdraws_the_offer_between_receipts_and_batch_0(tmp_path):
    wire = DoorWire(offers=True)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    wire.enabled = False  # the door's list changed after the receipts answer
    assert journal.stage(sid, cwd=CWD) is not None
    with pytest.raises(DeliveryPending):
        journal.deliver(sid, wire)
    _drain(journal, wire, sid)
    assert [b["protocol_version"] for b in wire.bodies(sid)] == [2]
    journal.close()


def test_other_409s_and_later_batches_never_restart(tmp_path):
    wire = DoorWire(offers=True)
    wire.refuse_batch0 = "batch does not continue the acknowledged source/event cursor"
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    staged = journal.stage(sid, cwd=CWD)
    with pytest.raises(ReconciliationRequired):
        journal.deliver(sid, wire)
    assert journal.pending(sid) == staged
    wire.refuse_batch0 = None
    journal.deliver(sid, wire)
    # Batch 1 of a stream the server pinned to 3: a refusal there is no restart.
    _write(path, [_user(sid, "later", 9)])
    second = journal.stage(sid, cwd=CWD)
    assert json.loads(second)["batch_seq"] == 1
    wire.streams[sid]["protocol_version"] = 2  # the door now says "protocol mismatch"
    with pytest.raises(ReconciliationRequired):
        journal.deliver(sid, wire)
    assert journal.pending(sid) == second and journal.get(sid)["protocol_version"] == 3
    journal.close()


# -- where protocol-3 sessions live ----------------------------------------------------


def test_taps_before_protocol_3_cannot_see_its_pinned_sessions(tmp_path):
    """They read only `sessions`, drain every row there, and delete every
    `*.snapshot.jsonl` their own rows do not name. A session moves out of
    their sight once the server holds it on protocol 3, not on the offer."""
    wire = DoorWire(offers=True)
    sid3, path3 = _session(tmp_path, name="three")
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid3, path3, historical=True)
    wire.offers = False  # this one's receipts answer offers protocol 2 only
    sid2, path2 = _session(tmp_path, name="two")
    _start(journal, wire, sid2, path2, historical=True)
    assert _tables(journal) == {"sessions": {sid2, sid3}, "fragment_sessions": set()}
    snapshot3 = Path(journal.get(sid3)["snapshot_path"])
    assert snapshot3.name.endswith(".snapshot-p3.jsonl") and snapshot3.exists()
    assert [p.name for p in journal.directory.glob("*.snapshot.jsonl")] == [
        Path(journal.get(sid2)["snapshot_path"]).name
    ]
    journal.deliver(sid3, wire) if journal.stage(sid3, cwd=CWD, historical_only=True) else None
    assert journal.get(sid3)["protocol_version"] == 3
    assert _tables(journal) == {"sessions": {sid2}, "fragment_sessions": {sid3}}
    assert {s["session_id"] for s in journal.sessions()} == {sid2, sid3}
    # Both drain and finish through this journal, each on its own protocol.
    _drain(journal, wire, sid3, historical_only=True)
    _drain(journal, wire, sid2, historical_only=True)
    assert [b["protocol_version"] for b in wire.bodies(sid3)] == [3, 3]  # data, then finalize
    assert [b["protocol_version"] for b in wire.bodies(sid2)] == [2, 2]
    assert journal.get(sid3)["historical_complete"] and journal.get(sid2)["historical_complete"]
    assert Path(journal.get(sid3)["snapshot_path"]) == snapshot3
    journal.close()


# -- an older tap or `probe import` on the same machine (tap 0.9.13) -----------------

_OLD_JOURNAL = _AGENT / "tests" / "fixtures" / "tap_0_9_13" / "session_journal.py"


def _old_journal_module():
    """Tap 0.9.13's journal, loaded beside this one (its relative imports
    resolve to today's sanitizers; the journal logic is 0.9.13's)."""
    spec = importlib.util.spec_from_file_location(
        "probe.tap_core._session_journal_0_9_13", _OLD_JOURNAL
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


OLD = _old_journal_module()


class OldWire(OLD.Wire):
    """0.9.13's own Wire, its receipts check included, answered by the door."""

    def __init__(self, door: DoorWire):
        super().__init__(door.base_url, door.token, door.source)
        self.door = door

    def _request(self, path, body=None):
        if body is None:
            return 200, self.door.receipts(path.split("?")[0].split("/")[-2])
        return self.door.post(body)


def _old_tick(journal, wire: OldWire, sid: str, path: Path, *, deliver=True) -> list[Exception]:
    """One pass of a 0.9.13 tap daemon (tap/main.py at e7993877b), reduced to
    what touches the journal: adopt the transcript if this journal does not
    know the session (the gap sweep), then drain every session it sees."""
    problems: list[Exception] = []
    if journal.get(sid) is None:
        try:
            journal.ensure(sid, path, wire.receipts(sid), historical=False, cwd=CWD)
        except (OLD.DeliveryPending, OLD.ReconciliationRequired) as exc:
            problems.append(exc)
    for state in journal.sessions():
        try:
            while journal.stage(state["session_id"], cwd=CWD) is not None:
                if not deliver:
                    break
                journal.deliver(state["session_id"], wire)
        except (OLD.DeliveryPending, OLD.ReconciliationRequired) as exc:
            problems.append(exc)
    return problems


def _settle(journal: Journal, wire, sid: str) -> list[Exception]:
    """This tap's drain, keeping what it could not deliver."""
    try:
        _drain(journal, wire, sid)
    except (DeliveryPending, ReconciliationRequired) as exc:
        return [exc]
    return []


def _one_stream(door: DoorWire, sid: str, *journals) -> str:
    """The session has exactly one stream: on the server, in every body the
    server took, and in every journal's state."""
    bodies = door.bodies(sid)
    streams = {b["stream_id"] for b in bodies} | {door.streams[sid]["stream_id"]}
    streams |= {j.get(sid)["stream_id"] for j in journals if j.get(sid) is not None}
    assert len(streams) == 1, streams
    assert not [c for c in door.calls if json.loads(c).get("stream_id") not in streams]
    return streams.pop()


@pytest.mark.parametrize("old_delivers", [True, False], ids=["old-delivers", "old-only-stages"])
def test_an_older_tap_and_this_one_settle_a_session_on_one_stream(tmp_path, old_delivers):
    """The new tap adopts a live session while protocol 3 is offered; a 0.9.13
    daemon (or `probe import`) on the same machine sweeps the same transcript
    before anything was sent. Both must continue ONE stream: hidden from the
    old one, the session got a second stream whose batches the new one then
    acknowledged as its own, and the next batch was refused forever (409
    `session owned by another stream`)."""
    door = DoorWire(offers=True)
    sid, path = _session(tmp_path, lines=[])
    new = _journal(tmp_path, door)
    _start(new, door, sid, path)  # live: the transcript is still empty
    _write(path, [_user(sid, f"turn {i}", i) for i in range(4)])
    old = OLD.Journal(door.base_url, CUSTOMER, door.source, directory=tmp_path / "state")
    old_wire = OldWire(door)
    problems = _old_tick(old, old_wire, sid, path, deliver=old_delivers)
    problems += _settle(new, door, sid)
    _write(path, [_user(sid, "later", 9)])
    problems += _old_tick(old, old_wire, sid, path)
    problems += _settle(new, door, sid)
    assert [str(p) for p in problems] == []
    stream = _one_stream(door, sid, new, old)
    assert old.get(sid) is not None  # an offer alone never hid the session
    assert door.streams[sid]["event_end"] == 5 and door.streams[sid]["last_seq"] >= 1
    assert all(b["protocol_version"] == 2 for b in door.bodies(sid))  # the old tap staged first
    # Recorded by whichever tap acknowledged; either way the stream is on 2.
    assert sj._stream_protocol(new.get(sid)) == 2 and new.get(sid)["stream_id"] == stream
    assert _tables(new) == {"sessions": {sid}, "fragment_sessions": set()}
    old.close()
    new.close()


def test_an_older_tap_meeting_a_staged_protocol_3_batch_leaves_one_stream(tmp_path):
    """This tap staged protocol-3 batch 0; a 0.9.13 tap sends that same body
    (the pending row is shared), cannot acknowledge a protocol-3 receipt, and
    once the server holds the stream on 3 never sees the session again."""
    door = DoorWire(offers=True)
    sid, path = _session(tmp_path)
    new = _journal(tmp_path, door)
    _start(new, door, sid, path)
    staged = new.stage(sid, cwd=CWD)
    assert json.loads(staged)["protocol_version"] == 3
    old = OLD.Journal(door.base_url, CUSTOMER, door.source, directory=tmp_path / "state")
    old_wire = OldWire(door)
    problems = _old_tick(old, old_wire, sid, path)
    assert [type(p).__name__ for p in problems] == ["ReconciliationRequired"]
    assert door.bodies(sid) == [json.loads(staged)]  # the server took the one body
    new.deliver(sid, door)  # a duplicate: the receipt settles it
    assert new.get(sid)["protocol_version"] == 3 and new.pending(sid) is None
    assert old.get(sid) is None
    _write(path, [_user(sid, "later", 9)])
    problems = _old_tick(old, old_wire, sid, path)  # its sweep: receipts say protocol 3
    assert [type(p).__name__ for p in problems] == ["DeliveryPending"] and old.get(sid) is None
    _drain(new, door, sid)
    _one_stream(door, sid, new)
    assert [b["protocol_version"] for b in door.bodies(sid)] == [3, 3]
    old.close()
    new.close()


@pytest.mark.parametrize("links", [True, False], ids=["hard-link", "copy"])
def test_a_snapshot_an_older_tap_froze_survives_the_move_out_of_its_view(tmp_path, monkeypatch, links):
    """A 0.9.13 tap froze an offered session's history (`pin_orphan`) as
    `*.snapshot.jsonl`. Once the server holds the session on protocol 3 it
    leaves that tap's view, and its next sweep deletes the file as an orphan:
    the move gives the same bytes the protocol-3 name first."""
    if not links:
        def refuse(*_args):
            raise OSError(18, "Invalid cross-device link")

        monkeypatch.setattr(sj.os, "link", refuse)
    door = DoorWire(offers=True)
    sid, path = _session(tmp_path)
    new = _journal(tmp_path, door)
    _start(new, door, sid, path)
    new.stage(sid, cwd=CWD)  # protocol-3 batch 0 staged; its daemon goes away
    old = OLD.Journal(door.base_url, CUSTOMER, door.source, directory=tmp_path / "state")
    old_wire = OldWire(door)
    assert old.pin_orphan(sid, old_wire.receipts(sid))
    frozen = Path(old.get(sid)["snapshot_path"])
    assert frozen.name.endswith(".snapshot.jsonl")
    new.deliver(sid, door)  # the server holds it on 3: it moves
    snapshot = Path(new.get(sid)["snapshot_path"])
    assert snapshot.name.endswith(".snapshot-p3.jsonl") and snapshot.read_bytes() == frozen.read_bytes()
    assert old.get(sid) is None
    other, other_path = _session(tmp_path, name="other")
    old.ensure(other, other_path, old_wire.receipts(other), historical=False, cwd=CWD)
    assert not frozen.exists() and snapshot.exists()  # the old tap swept its orphan
    _drain(new, door, sid, historical_only=True)
    assert new.get(sid)["historical_complete"]
    assert [b["protocol_version"] for b in door.bodies(sid)] == [3, 3]
    old.close()
    new.close()


def test_a_pending_batch_of_another_stream_is_never_acknowledged_as_this_one(tmp_path):
    wire = DoorWire(offers=False)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    payload = json.loads(journal.stage(sid, cwd=CWD))
    payload["stream_id"] = str(uuid.uuid4())  # another producer's reservation
    foreign = canonical_payload(payload)
    journal.conn.execute(
        "UPDATE pending SET body=?, digest=? WHERE session_id=?",
        (foreign, hashlib.sha256(foreign).hexdigest(), sid),
    )
    before = journal.get(sid)
    code, result = wire.post(foreign)
    assert code == 202
    with pytest.raises(ReconciliationRequired, match="another stream"):
        journal.acknowledge(sid, result, sent_body=foreign)
    assert journal.get(sid) == before and journal.pending(sid) == foreign
    journal.close()


# -- protocol 2 retired for new streams: a pending protocol-2 batch 0 goes on 3 -------
# Gate 2 of #2454 (engine `SESSION_PROTOCOL2_NEW_STREAMS=false`). A session an
# older tap staged on protocol 2, and the server never took, is refused at batch
# 0 for good: the journal drops that batch and sends the session again from batch
# 0 on protocol 3, under the same stream id.


def _retire_protocol2(door: DoorWire, *, events: bool = False) -> None:
    """Gate 2 at the door: protocol 3 offered and enabled, protocol 2 retired
    for new streams."""
    door.offer(True)
    door.events = events
    door.protocol2_new_streams = False


def _old_staged(tmp_path, door: DoorWire, sid: str, path: Path, *, historical: bool = False):
    """A tap 0.9.13 journal on this machine stages the session's protocol-2
    batch 0 and never gets it to the server (offline, or the door changed)."""
    old = OLD.Journal(door.base_url, CUSTOMER, door.source, directory=tmp_path / "state")
    old_wire = OldWire(door)
    old.ensure(sid, path, old_wire.receipts(sid), historical=False, cwd=CWD)
    if historical:  # its daemon died: the orphan sweep froze the history
        assert old.pin_orphan(sid, old_wire.receipts(sid))
    staged = old.stage(sid, cwd=CWD, historical_only=historical)
    assert json.loads(staged)["protocol_version"] == 2 and json.loads(staged)["batch_seq"] == 0
    return old, old_wire, staged


def _fragment_ordinals(door: DoorWire, sid: str) -> list[int]:
    return [f["line"]["line_no"] for b in door.bodies(sid) for f in b.get("fragments", [])]


def test_the_retired_detail_is_the_doors():
    """prbe-knowledge `kb/session_receipts.py` `PROTOCOL2_RETIRED`, matched as text."""
    assert sj.PROTOCOL2_RETIRED == "protocol 2 retired"
    assert sj.PROTOCOL2_RETIRED not in sj.PROTOCOL3_REFUSALS


def test_the_door_offers_protocol_2_until_retired_and_only_where_3_replaces_it():
    """The fake follows the engine's `accepts`: 2 leaves the offer only while
    protocol 3 is offered (the kill switch re-opens it)."""
    door = DoorWire(offers=True)
    sid = str(uuid.uuid4())
    assert door.receipts(sid)["accepts"]["protocols"] == [2, 3]
    door.protocol2_new_streams = False
    answer = door.receipts(sid)
    assert answer["accepts"]["protocols"] == [3] and answer["protocol_version"] == 2
    assert sj.negotiate(answer) == (3, False)
    door.offer(False)
    assert door.receipts(sid)["accepts"]["protocols"] == [2]


@pytest.mark.parametrize("events", [False, True], ids=["fragments", "fragments+events"])
@pytest.mark.parametrize("historical", [False, True], ids=["live", "historical"])
def test_an_older_taps_pending_protocol_2_batch_0_is_sent_again_on_3(tmp_path, historical, events):
    """The gap #2454 names: refused for good, the pending protocol-2 batch 0
    is dropped and the WHOLE session goes up on protocol 3, same stream id."""
    door = DoorWire(offers=False)  # before the update: protocol 2 only
    sid, path = _long_session(tmp_path)
    old, old_wire, staged = _old_staged(tmp_path, door, sid, path, historical=historical)
    stream = json.loads(staged)["stream_id"]
    _retire_protocol2(door, events=events)
    # The older tap keeps the refused batch and re-sends it: nothing lost, nothing sent.
    with pytest.raises(OLD.ReconciliationRequired):
        old.deliver(sid, old_wire)
    assert old.pending(sid) == staged and door.accepted == {}

    new = _journal(tmp_path, door)  # the machine updated
    with pytest.raises(sj.ProtocolRestarted) as restarted:
        new.deliver(sid, door)
    assert restarted.value.protocol == 3 and restarted.value.retryable
    assert "restarts on protocol 3" in str(restarted.value)
    state = new.get(sid)
    assert new.pending(sid) is None and state["stream_id"] == stream
    assert state["protocol_offer"] == 3 and state["send_events"] is events
    assert state.get("protocol_version") is None and state["last_seq"] == -1
    assert (state["source_byte_end"], state["source_line_end"], state["event_end"]) == (0, 0, 0)
    # Offered only: still where older taps see it, so none starts a second stream.
    assert _tables(new) == {"sessions": {sid}, "fragment_sessions": set()}
    if historical:
        snapshot = Path(state["snapshot_path"])
        assert snapshot.name.endswith(".snapshot-p3.jsonl")
        assert snapshot.read_bytes() == path.read_bytes()

    _drain(new, door, sid, max_body_bytes=12_000, historical_only=historical)
    bodies = door.bodies(sid)
    assert len(bodies) > 2 and {b["protocol_version"] for b in bodies} == {3}
    assert all(json.loads(c)["protocol_version"] == 2 for c in door.calls[:2])  # both refusals
    assert _fragment_ordinals(door, sid) == list(range(12))
    assert door.streams[sid] | {"finalized": None} == door.streams[sid] | {
        "stream_id": stream, "protocol_version": 3, "source_byte_end": path.stat().st_size,
        "event_end": 12, "finalized": None,
    }
    assert all(("events" in b) is events for b in bodies if not b.get("finalize"))
    assert new.get(sid)["protocol_version"] == 3
    assert _tables(new) == {"sessions": set(), "fragment_sessions": {sid}}
    if historical:
        assert bodies[-1]["finalize"] and new.get(sid)["historical_complete"]
        assert {b["snapshot_byte_end"] for b in bodies} == {path.stat().st_size}
    _one_stream(door, sid, new)
    old.close()
    new.close()


def test_an_open_protocol_2_stream_keeps_protocol_2_after_the_retirement(tmp_path):
    """Open protocol-2 streams finish on 2: a later batch, a lost response's
    replay of batch 0, and another device adopting the stream."""
    door = DoorWire(offers=False)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, door)
    _start(journal, door, sid, path)
    first = journal.stage(sid, cwd=CWD)
    assert door.post(first)[0] == 202  # the server took batch 0; the answer was lost
    _retire_protocol2(door)
    journal.deliver(sid, door)  # a duplicate: settled by its receipt, no restart
    assert journal.get(sid)["protocol_version"] == 2 and journal.pending(sid) is None
    _write(path, [_user(sid, "after the retirement", 9)])
    _drain(journal, door, sid)
    other = _journal(tmp_path, door, name="other-device")
    _write(path, [_user(sid, "on another device", 10)])
    _start(other, door, sid, path)
    _drain(other, door, sid)
    assert [b["protocol_version"] for b in door.bodies(sid)] == [2, 2, 2]
    assert door.streams[sid]["protocol_version"] == 2 and door.streams[sid]["event_end"] == 8
    assert all(door.post(c)[0] == 202 for c in list(door.calls))  # nothing was refused
    journal.close()
    other.close()


def test_a_protocol_3_session_is_untouched_by_the_retirement(tmp_path):
    door = DoorWire(offers=True)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, door)
    _start(journal, door, sid, path)
    _drain(journal, door, sid)
    _retire_protocol2(door)
    _write(path, [_user(sid, "after the retirement", 9)])
    _drain(journal, door, sid)
    assert [b["protocol_version"] for b in door.bodies(sid)] == [3, 3]
    assert len(door.calls) == 2  # nothing refused, nothing restarted
    journal.close()


def test_the_restart_survives_a_tap_restart_and_a_lost_response(tmp_path):
    """Idempotent: the process dies after the restart, then after the server
    took protocol-3 batch 0 but before its answer arrived. One stream, one
    protocol-3 batch 0, and the old protocol-2 bytes are never acknowledged."""
    door = DoorWire(offers=False)
    sid, path = _session(tmp_path)
    old, _old_wire, staged = _old_staged(tmp_path, door, sid, path)
    _retire_protocol2(door)
    first = _journal(tmp_path, door)
    with pytest.raises(sj.ProtocolRestarted):
        first.deliver(sid, door)
    first.close()  # dies before staging again

    second = _journal(tmp_path, door)
    batch0 = second.stage(sid, cwd=CWD)
    assert json.loads(batch0)["protocol_version"] == 3 and json.loads(batch0)["batch_seq"] == 0
    # A stale caller still holding the protocol-2 bytes changes nothing.
    with pytest.raises(ReconciliationRequired):
        second.deliver(sid, door, expected_body=staged)
    assert second.pending(sid) == batch0 and second.get(sid)["protocol_offer"] == 3
    assert door.post(batch0)[0] == 202  # the server took it; the answer was lost
    second.close()

    third = _journal(tmp_path, door)
    assert third.stage(sid, cwd=CWD) == batch0  # the same immutable bytes
    third.deliver(sid, door)
    _write(path, [_user(sid, "later", 9)])
    _drain(third, door, sid)
    assert [b["protocol_version"] for b in door.bodies(sid)] == [3, 3]
    assert sorted(
        json.loads(c)["batch_seq"] for c in door.calls if json.loads(c)["protocol_version"] == 3
    ) == [0, 0, 1]
    assert third.get(sid)["protocol_version"] == 3 and door.streams[sid]["event_end"] == 7
    _one_stream(door, sid, third)
    old.close()
    third.close()


@pytest.mark.parametrize("why", ["no-builder", "server-holds-a-stream", "not-offered"])
def test_a_retired_batch_0_waits_when_there_is_nothing_to_restart_on(tmp_path, monkeypatch, why):
    """No restart unless the session can go on protocol 3 and the server holds
    nothing for it: the batch stays pending (retried, never dropped)."""
    door = DoorWire(offers=False)
    sid, path = _session(tmp_path)
    old, _old_wire, staged = _old_staged(tmp_path, door, sid, path)
    _retire_protocol2(door)
    if why == "no-builder":
        monkeypatch.setattr(sj, "_fragment_module", lambda: None)
    elif why == "not-offered":  # an answer without protocol 3 (an engine without the coupling)
        monkeypatch.setattr(
            door, "receipts",
            lambda sid, **kw: DoorWire.receipts(door, sid, **kw) | {"accepts": {"protocols": []}},
        )
    else:  # between the refusal and the receipts read another device started it
        held = {"state": "ready", "stream": {"stream_id": str(uuid.uuid4()), "last_seq": 0}}
        monkeypatch.setattr(
            door, "receipts", lambda sid, **kw: DoorWire.receipts(door, sid, **kw) | held
        )
    journal = _journal(tmp_path, door)
    before = journal.get(sid)
    with pytest.raises(ReconciliationRequired) as refused:
        journal.deliver(sid, door)
    assert refused.value.status_code == 409 and sj.recoverable(refused.value)
    assert journal.pending(sid) == staged
    assert {k: v for k, v in journal.get(sid).items() if k != "error"} == {
        k: v for k, v in before.items() if k != "error"
    }
    assert door.accepted == {}
    old.close()
    journal.close()


def test_a_retired_batch_0_of_a_deleted_session_is_settled_as_deleted(tmp_path):
    door = DoorWire(offers=False)
    sid, path = _session(tmp_path)
    old, _old_wire, _staged = _old_staged(tmp_path, door, sid, path)
    _retire_protocol2(door)
    journal = _journal(tmp_path, door)
    door.receipts = lambda s, **kw: DoorWire.receipts(door, s, **kw) | {"state": "deleted"}
    with pytest.raises(sj.SessionDeleted):
        journal.deliver(sid, door)
    assert journal.pending(sid) is None and journal.is_deleted(sid)
    old.close()
    journal.close()


@pytest.mark.parametrize("old_stages_in_the_gap", [False, True], ids=["old-resends-p3", "old-restages-p2"])
def test_an_older_tap_beside_the_restart_leaves_one_stream(tmp_path, old_stages_in_the_gap):
    """A 0.9.13 daemon still running on the machine drains the same session.
    Either it re-sends the staged protocol-3 batch 0 (the server takes it once,
    it cannot acknowledge it), or it stages protocol 2 again in the gap before
    this tap re-stages (refused, restarted again). One stream either way, and
    once the server holds it on 3 the older tap never sees it again."""
    door = DoorWire(offers=False)
    sid, path = _session(tmp_path)
    old, old_wire, _staged = _old_staged(tmp_path, door, sid, path)
    _retire_protocol2(door)
    new = _journal(tmp_path, door)
    with pytest.raises(sj.ProtocolRestarted):
        new.deliver(sid, door)
    if old_stages_in_the_gap:
        problems = _old_tick(old, old_wire, sid, path)
        assert [type(p).__name__ for p in problems] == ["ReconciliationRequired"]
        assert json.loads(new.pending(sid))["protocol_version"] == 2
        assert [type(p).__name__ for p in _settle(new, door, sid)] == ["ProtocolRestarted"]
    else:
        new.stage(sid, cwd=CWD)
        problems = _old_tick(old, old_wire, sid, path)
        assert [type(p).__name__ for p in problems] == ["ReconciliationRequired"]
    assert _settle(new, door, sid) == []
    assert old.get(sid) is None  # pinned to 3: out of the older tap's view
    _write(path, [_user(sid, "later", 9)])
    problems = _old_tick(old, old_wire, sid, path)  # its gap sweep: receipts say protocol 3
    assert [type(p).__name__ for p in problems] == ["DeliveryPending"] and old.get(sid) is None
    assert _settle(new, door, sid) == []
    _one_stream(door, sid, new)
    assert [b["protocol_version"] for b in door.bodies(sid)] == [3, 3]
    assert door.streams[sid]["event_end"] == 7
    old.close()
    new.close()


# -- the batch (§2, §3) --------------------------------------------------------------


@pytest.mark.parametrize("events", [False, True], ids=["fragments", "fragments+events"])
@pytest.mark.parametrize("harness", HARNESSES)
def test_fragments_are_the_vendored_builders_over_the_scrubbed_events(tmp_path, harness, events):
    """Per harness, from the probe-events/1 goldens: the batch's fragments are
    `fragment(event)` of the scrubbed events, one per ordinal, and the events
    go beside them only when the server asked."""
    wire = DoorWire(harness, offers=True, events=events)
    sid = str(uuid.uuid4())
    path = tmp_path / f"{sid}.jsonl"
    path.write_bytes((GOLDENS / harness / "raw.jsonl").read_bytes())
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    (body,) = wire.bodies(sid)  # one batch, so its scrub is the whole session's
    golden = [
        json.loads(line)
        for line in (GOLDENS / harness / "expected.jsonl").read_text().splitlines()
        if line.strip()
    ]
    expected_events = _flatten(golden)
    assert body["event_start"] == 0 and body["event_end"] == len(expected_events) > 0
    assert body["fragments"] == _expected_fragments(expected_events)
    assert [f["line"]["line_no"] for f in body["fragments"]] == list(range(len(expected_events)))
    if events:
        assert body["events"] == sj._scrub_content({"events": expected_events})["events"]
    else:
        assert "events" not in body
    assert body["fragment_version"] == atif_fragment.FRAGMENT_VERSION == 1
    journal.close()


def test_finalize_carries_the_fragment_version_and_nothing_else(tmp_path):
    wire = DoorWire(offers=True, events=True)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    _drain(journal, wire, sid, finalize=True)
    data, final = wire.bodies(sid)
    assert final["finalize"] is True and final["protocol_version"] == 3
    assert final["fragment_version"] == atif_fragment.FRAGMENT_VERSION
    assert not {"fragments", "events", "cwd"} & final.keys()
    assert final["event_start"] == final["event_end"] == data["event_end"]
    assert journal.get(sid)["finalized"]
    journal.close()


def test_a_fragment_that_raises_still_covers_its_ordinal(tmp_path, monkeypatch):
    real = atif_fragment.fragment

    def flaky(event):
        if event["line_no"] == 1:
            raise RuntimeError("synthetic")
        return real(event)

    monkeypatch.setattr(atif_fragment, "fragment", flaky)
    wire = DoorWire(offers=True)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    (body,) = wire.bodies(sid)
    assert [f["line"]["line_no"] for f in body["fragments"]] == list(range(6))
    assert body["fragments"][1] == {"v": 1, "line": {"line_no": 1, "text": ""}, "error": "RuntimeError"}
    assert body["fragments"][0]["kind"] == "user"
    journal.close()


def test_memory_error_is_never_sent_as_an_empty_fragment(tmp_path, monkeypatch):
    def exhausted(event):
        raise MemoryError

    monkeypatch.setattr(atif_fragment, "fragment", exhausted)
    wire = DoorWire(offers=True)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    with pytest.raises(MemoryError):
        journal.stage(sid, cwd=CWD)
    assert journal.pending(sid) is None and journal.get(sid)["source_byte_end"] == 0
    journal.close()


def test_a_protocol_3_stream_without_its_builder_keeps_the_source(tmp_path, monkeypatch):
    wire = DoorWire(offers=True)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    monkeypatch.setattr(sj, "_fragment_module", lambda: None)
    with pytest.raises(DeliveryPending, match="protocol 3"):
        journal.stage(sid, cwd=CWD)
    assert journal.pending(sid) is None and journal.get(sid)["source_byte_end"] == 0
    journal.close()


# -- packing (R9) --------------------------------------------------------------------


def _long_session(tmp_path, count=12, size=1500):
    sid = str(uuid.uuid4())
    lines = [_assistant(sid, f"{i:04d} " + "x" * size, i) for i in range(count)]
    return sid, _write(tmp_path / f"{sid}.jsonl", lines)


def test_batches_are_packed_by_fragment_size(tmp_path):
    limit = 9000
    sid, path = _long_session(tmp_path)
    p2, p3 = DoorWire(offers=False), DoorWire(offers=True)
    for wire, name in ((p2, "two"), (p3, "three")):
        journal = _journal(tmp_path, wire, name=name)
        _start(journal, wire, sid, path)
        sent = _drain(journal, wire, sid, max_body_bytes=limit)
        assert all(len(body) <= limit for body in sent)
        journal.close()
    events_per_batch = [b["event_end"] - b["event_start"] for b in p2.bodies(sid)]
    fragments_per_batch = [len(b["fragments"]) for b in p3.bodies(sid)]
    # A fragment carries its text twice (its Line and its part): half as many fit.
    assert max(fragments_per_batch) < max(events_per_batch)
    assert sum(fragments_per_batch) == sum(events_per_batch) == 12
    # Packed by each line's fragment estimate (2048 bytes are the envelope
    # reserve): the first batch holds exactly the lines whose estimates fit.
    events = [e for b in p2.bodies(sid) for e in b["events"]]
    sizes = [sj._record_bytes([e])[0] for e in events]
    first = fragments_per_batch[0]
    assert 2048 + sum(sizes[:first]) <= limit < 2048 + sum(sizes[:first + 1])


def test_the_built_batch_is_measured_not_the_estimate(tmp_path, monkeypatch):
    """Packing estimates each line before scrubbing; the staged batch is
    measured as sent. An estimate that is far too low still never stages an
    oversized batch: lines are given back until it fits."""
    real = sj._record_bytes
    monkeypatch.setattr(sj, "_record_bytes", lambda *args: tuple(n // 3 for n in real(*args)))
    limit = 9000
    sid, path = _long_session(tmp_path)
    wire = DoorWire(offers=True)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    sent = _drain(journal, wire, sid, max_body_bytes=limit)
    assert len(sent) > 2 and all(len(body) <= limit for body in sent)
    ordinals = [f["line"]["line_no"] for b in wire.bodies(sid) for f in b["fragments"]]
    assert ordinals == list(range(12))
    journal.close()


@pytest.mark.parametrize("events", [False, True])
def test_a_record_packed_alone_is_held_to_the_budget_by_its_fragments(tmp_path, events):
    """A line packed alone may use the route budget (`solo_limit`). Events are
    optional per protocol-3 batch, so a record whose event does not fit beside
    its fragments goes without it; one whose fragments alone do not fit keeps
    its source, as protocol 2 does with an event."""
    sid = str(uuid.uuid4())
    path = _write(tmp_path / f"{sid}.jsonl", [_assistant(sid, "y" * 7000), _assistant(sid, "z" * 12000, 1)])
    wire = DoorWire(offers=True, events=events)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    stage = {"max_body_bytes": 4096, "solo_limit": 20_000}
    # ~14 KB of fragment (+ ~7 KB of event): goes alone, without its event.
    body = json.loads(journal.stage(sid, cwd=CWD, **stage))
    assert 4096 < len(canonical_payload(body)) <= 20_000 and len(body["fragments"]) == 1
    assert "events" not in body
    journal.deliver(sid, wire)
    # ~24 KB of fragment alone: over the budget, the source is retained.
    end = journal.get(sid)["source_byte_end"]
    with pytest.raises(DeliveryPending, match="exceeds"):
        journal.stage(sid, cwd=CWD, **stage)
    assert journal.pending(sid) is None and journal.get(sid)["source_byte_end"] == end
    journal.close()


def test_packing_never_builds_a_fragment_twice(tmp_path, monkeypatch):
    """Lines are packed by an estimate from their events; each fragment is
    built once, for the batch that sends it."""
    built = []
    real = atif_fragment.fragment
    monkeypatch.setattr(atif_fragment, "fragment", lambda event: built.append(event["line_no"]) or real(event))
    sid, path = _long_session(tmp_path)
    wire = DoorWire(offers=True)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid, max_body_bytes=9000)
    assert len(wire.bodies(sid)) > 2 and sorted(built) == list(range(12))
    journal.close()


def test_each_protocol_packs_to_its_own_target(tmp_path, monkeypatch):
    """Protocol 3 carries the same events in about twice the bytes, so its
    default packing target is twice protocol 2's (read when staging)."""
    assert sj.MAX_FRAGMENT_BODY_BYTES == 2 * sj.MAX_BODY_BYTES
    monkeypatch.setattr(sj, "MAX_BODY_BYTES", 6000)
    monkeypatch.setattr(sj, "MAX_FRAGMENT_BODY_BYTES", 12000)
    sid, path = _long_session(tmp_path)
    sizes = {}
    for offers in (False, True):
        wire = DoorWire(offers=offers)
        journal = _journal(tmp_path, wire, name=f"state-{offers}")
        _start(journal, wire, sid, path)
        sizes[offers] = [len(body) for body in _drain(journal, wire, sid)]
        journal.close()
    assert max(sizes[False]) <= 6000 < max(sizes[True]) <= 12000


def test_a_lone_record_is_judged_on_its_exact_fragment_when_the_estimate_is_over(tmp_path):
    """The estimate (twice the event) is only for packing: a lone record whose
    estimate is over the route budget is measured exactly before it is held
    back. A harness reminder costs an event its bytes and a fragment nothing."""
    sid = str(uuid.uuid4())
    reminder = "<system-reminder>" + "r" * 9000 + "</system-reminder>"
    path = _write(tmp_path / f"{sid}.jsonl", [_user(sid, "hi " + reminder)])
    wire = DoorWire(offers=True)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    events = [{"line_no": 0, "raw": json.loads(path.read_text())}]
    assert sj._record_bytes(events)[0] > 15_000
    body = json.loads(journal.stage(sid, cwd=CWD, max_body_bytes=4096, solo_limit=15_000))
    assert body["fragments"][0]["message"] == "hi"
    journal.close()


def test_each_protocol_has_its_own_route_budget(tmp_path, monkeypatch):
    """The gateway takes 6 MB for a protocol-3 batch (one event's text can ride
    three times) and 2 MB for protocol 2; a lone record is held to its own."""
    assert sj.SERVER_BATCH_LIMIT == 2_000_000 and sj.SERVER_FRAGMENT_BATCH_LIMIT == 6_000_000
    assert sj.MAX_SOLO_FRAGMENT_BYTES == sj.SERVER_FRAGMENT_BATCH_LIMIT - sj.ENVELOPE_HEADROOM
    # Scaled down (the defaults are read when staging): an event of ~12 KB
    # whose fragment is ~24 KB.
    monkeypatch.setattr(sj, "MAX_SOLO_EVENT_BYTES", 10_000)
    monkeypatch.setattr(sj, "MAX_SOLO_FRAGMENT_BYTES", 30_000)
    outcomes = {}
    for offers in (False, True):
        sid = str(uuid.uuid4())
        path = _write(tmp_path / f"{sid}.jsonl", [_assistant(sid, "w" * 12000)])
        wire = DoorWire(offers=offers)
        journal = _journal(tmp_path, wire, name=f"state-{offers}")
        _start(journal, wire, sid, path)
        try:
            outcomes[offers] = len(journal.stage(sid, cwd=CWD, max_body_bytes=4096))
        except DeliveryPending:
            outcomes[offers] = None
        journal.close()
    assert outcomes[False] is None and 20_000 < outcomes[True] <= 30_000


# -- restart determinism -------------------------------------------------------------


def test_a_restarted_tap_sends_the_same_bytes(tmp_path, monkeypatch):
    """Receipts pin request bytes: whether one process uploads a session, or a
    process per batch with a lost response in between, every batch is the same
    bytes for the same source bytes."""
    sid = str(uuid.uuid4())
    stream = uuid.UUID("00000000-0000-4000-8000-0000000000a5")
    monkeypatch.setattr(sj.uuid, "uuid4", lambda: stream)  # the same stream id in both runs
    path = tmp_path / f"{sid}.jsonl"
    path.write_bytes((GOLDENS / "claude_code" / "raw.jsonl").read_bytes())
    stage = {"max_body_bytes": 6000}

    one = DoorWire(offers=True, events=True)
    journal = _journal(tmp_path, one, name="one")
    _start(journal, one, sid, path)
    _drain(journal, one, sid, **stage)
    journal.close()

    many = DoorWire(offers=True, events=True)
    first = _journal(tmp_path, many, name="many")
    _start(first, many, sid, path)
    first.close()
    lost = False
    while True:
        journal = _journal(tmp_path, many, name="many")
        body = journal.stage(sid, cwd=CWD, **stage)
        if body is None:
            journal.close()
            break
        if not lost:  # the server takes it, the answer never arrives, the tap dies
            assert many.post(body)[0] == 202
            lost = True
            journal.close()
            continue
        journal.deliver(sid, many)
        journal.close()

    assert len(one.accepted) > 2
    assert list(one.accepted.values()) == list(many.accepted.values())
    assert sorted(json.loads(b)["batch_seq"] for b in many.calls) == [0, 0, *range(1, len(many.accepted))]


# -- scrubbing (R8) ------------------------------------------------------------------


def test_a_credential_split_across_two_prompts_leaves_no_fragment_holding_half(tmp_path):
    """Split across two user events: the events are scrubbed together before
    any fragment is built, so neither half reaches a fragment's prose or Line."""
    sid = str(uuid.uuid4())
    lines = [_user(sid, "here it is " + GITHUB[:20], 0), _user(sid, GITHUB[20:] + " thanks", 1)]
    path = _write(tmp_path / f"{sid}.jsonl", lines)
    wire = DoorWire(offers=True, events=True)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)  # deliver re-checks the body is a scrub fixed point
    (body,) = wire.bodies(sid)
    sent = json.dumps(body)
    assert GITHUB[:20] not in sent and GITHUB[20:] not in sent
    assert "<redacted:" in body["fragments"][0]["message"]
    assert body["fragments"][0]["line"]["text"].startswith("USER: here it is <redacted:")
    journal.close()


def test_a_credential_split_across_two_assistant_messages_is_redacted_in_the_fragments(tmp_path):
    """Two assistant events with text blocks (#2407 joins their blocks, and
    the fragments' text parts): no half reaches a fragment, and the batch is
    already a scrub fixed point."""
    sid = str(uuid.uuid4())
    lines = [_assistant(sid, "push with " + GITHUB[:15], 0), _assistant(sid, GITHUB[15:] + " now", 1)]
    path = _write(tmp_path / f"{sid}.jsonl", lines)
    wire = DoorWire(offers=True)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    (body,) = wire.bodies(sid)
    sent = json.dumps(body["fragments"])
    assert GITHUB[:15] not in sent and GITHUB[15:] not in sent
    assert sj._scrub_content(body) == body
    journal.close()


def test_a_pending_protocol_3_body_with_a_credential_in_a_fragment_is_refused(tmp_path):
    wire = DoorWire(offers=True)
    sid, path = _session(tmp_path)
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    staged = json.loads(journal.stage(sid, cwd=CWD))
    staged["fragments"][0]["message"] = "token " + GITHUB
    tampered = canonical_payload(staged)
    journal.conn.execute(
        "UPDATE pending SET body=?, digest=? WHERE session_id=?",
        (tampered, hashlib.sha256(tampered).hexdigest(), sid),
    )
    with pytest.raises(sj.UnsafePending):
        journal.deliver(sid, wire)
    assert wire.calls == []
    journal.close()


# -- the importer (backfill) uses the same journal -----------------------------------


def test_the_importer_uploads_on_protocol_3_when_offered(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    wire = DoorWire(offers=True)
    monkeypatch.setattr(bt, "Wire", lambda *args, **kwargs: wire)
    transcript = _transcript(tmp_path)
    poster = bt.Poster(wire.base_url, wire.token)
    record = bt.SessionRecord(session_id=transcript.session_id)
    result = bt.upload_session(transcript, record, poster, device_id="")
    assert result.ok and record.finalized, result.error
    bodies = wire.bodies(transcript.session_id)
    assert [b["protocol_version"] for b in bodies] == [3] * len(bodies) and bodies[-1]["finalize"]
    assert sum(len(b.get("fragments", [])) for b in bodies) == bodies[-1]["event_end"] == 12
    assert result.error is None
    # A finished protocol-3 stream is proof of coverage for the next import.
    again = bt.upload_session(transcript, bt.SessionRecord(session_id=transcript.session_id), poster,
                              device_id="")
    assert again.ok and again.already_finalized


def test_the_importer_restarts_a_refused_batch_0_on_protocol_2_in_the_same_run(tmp_path, monkeypatch):
    """A refusal at batch 0 is settled inline: the import neither fails nor
    reports a retryable error (which pauses a whole `probe import` run)."""
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    wire = DoorWire(offers=True)
    wire.enabled = False  # offered by the receipts answer, refused by the door
    monkeypatch.setattr(bt, "Wire", lambda *args, **kwargs: wire)
    transcript = _transcript(tmp_path)
    record = bt.SessionRecord(session_id=transcript.session_id)
    result = bt.upload_session(transcript, record, bt.Poster(wire.base_url, wire.token), device_id="")
    assert result.ok and result.error is None and not result.retryable and record.finalized
    assert json.loads(wire.calls[0])["protocol_version"] == 3  # the refused offer
    bodies = wire.bodies(transcript.session_id)
    assert {b["protocol_version"] for b in bodies} == {2} and bodies[-1]["finalize"]


def test_an_import_budget_below_protocol_3s_target_still_sends(tmp_path, monkeypatch):
    """`probe import --transcripts-budget-mb N` stops before a batch that would
    pass the budget. Protocol 3 packs toward twice protocol 2's target, so a
    budget between the two must cap it, or no batch ever fits (scaled down)."""
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    monkeypatch.setattr(sj, "MAX_FRAGMENT_BODY_BYTES", 40_000)
    wire = DoorWire(offers=True)
    monkeypatch.setattr(bt, "Wire", lambda *args, **kwargs: wire)
    sid, path = _long_session(tmp_path)  # 12 lines, ~38 KB of fragments
    transcript = bt.Transcript(path, sid, "claude_code", CWD, path.stat().st_size, path.stat().st_mtime)
    record = bt.SessionRecord(session_id=sid)
    poster = bt.Poster(wire.base_url, wire.token)
    result = bt.upload_session(transcript, record, poster, device_id="", budget_bytes=20_000)
    assert result.ok and result.error == "budget"
    assert result.batches >= 1 and 0 < result.bytes_sent <= 20_000
    assert all(len(body) <= 20_000 for body in wire.accepted.values())


def test_the_importer_sends_a_retired_protocol_2_batch_0_again_on_3_in_the_same_run(
    tmp_path, monkeypatch
):
    """`probe import` shares the journal: a protocol-2 batch 0 an earlier run
    staged and never delivered is restarted on protocol 3 inline."""
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    door = DoorWire(offers=False)
    monkeypatch.setattr(bt, "Wire", lambda *args, **kwargs: door)
    transcript = _transcript(tmp_path)
    poster = bt.Poster(door.base_url, door.token)
    monkeypatch.setattr(door, "post", lambda body: (503, {"detail": "unavailable"}))
    first = bt.upload_session(
        transcript, bt.SessionRecord(session_id=transcript.session_id), poster, device_id=""
    )
    assert not first.ok and first.retryable  # protocol-2 batch 0 left pending
    monkeypatch.setattr(door, "post", lambda body: DoorWire.post(door, body))
    _retire_protocol2(door)
    record = bt.SessionRecord(session_id=transcript.session_id)
    result = bt.upload_session(transcript, record, poster, device_id="")
    assert result.ok and result.error is None and record.finalized
    assert json.loads(door.calls[0])["protocol_version"] == 2  # the refused batch 0
    bodies = door.bodies(transcript.session_id)
    assert {b["protocol_version"] for b in bodies} == {3} and bodies[-1]["finalize"]
    assert bodies[-1]["event_end"] == 12


def test_the_importer_stops_restarting_a_session_whose_server_flips(tmp_path, monkeypatch):
    """Both refusals at once (protocol 3 refused at batch 0, protocol 2
    retired) would restart forever; the run gives up after
    MAX_PROTOCOL_RESTARTS and the session waits for a later run."""
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    door = DoorWire(offers=True)
    door.refuse_batch0 = "protocol 3 not enabled"
    door.protocol2_new_streams = False
    monkeypatch.setattr(bt, "Wire", lambda *args, **kwargs: door)
    transcript = _transcript(tmp_path)
    result = bt.upload_session(
        transcript, bt.SessionRecord(session_id=transcript.session_id),
        bt.Poster(door.base_url, door.token), device_id="",
    )
    assert not result.ok and result.retryable and "left for the next import" in result.error
    assert "sent again" not in result.error
    assert len(door.calls) == bt.MAX_PROTOCOL_RESTARTS + 1 and door.accepted == {}
