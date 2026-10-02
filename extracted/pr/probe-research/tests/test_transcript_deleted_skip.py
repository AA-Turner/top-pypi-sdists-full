"""A session its team had deleted is a SKIP for the import, and final.

The engine refuses a deleted session with 410 {"detail": {"reason":
"session_deleted"}} on the upload door and answers its receipts read with
`state: "deleted"`; the research-os gateway passes both through unchanged. The
import must not upload it, must not count it as a failure (nothing can fix it),
and must leave the shared transcript journal saying so, so the live tap never
sends it either.

These tests talk to a real HTTP server on localhost through the real `Wire`,
so the requests and response bodies are the ones production exchanges.
"""

from __future__ import annotations

import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from uuid import uuid4

import pytest
from probe.cli import backfill_transcripts as bt
from probe.tap_core.session_journal import Journal

from test_backfill_transcripts_upload import _transcript

CUSTOMER = "tenant-synthetic"


@pytest.fixture(autouse=True)
def isolated_state(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))


def _deleted_body(sid: str) -> dict:
    return {
        "detail": {
            "reason": "session_deleted",
            "message": "this session was deleted at the customer's request; do not resend it",
            "source": "claude_code",
            "session_id": sid,
        }
    }


class Gateway:
    """The two ingest routes the import uses, with a set of deleted sessions."""

    def __init__(self):
        self.requests: list[tuple[str, str, bytes]] = []
        self.deleted: set[str] = set()
        #: Sessions whose deletion lands after the receipts read (410 on upload).
        self.deleted_on_upload: set[str] = set()
        self.receipts_410 = False
        #: Force the upload answer: (status, body).
        self.upload_answer: tuple[int, dict] | None = None
        self.streams: dict[str, dict] = {}
        gateway = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def _answer(self, status, body):
                data = json.dumps(body).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                gateway.requests.append(("GET", self.path, b""))
                parts = self.path.split("?")[0].split("/")
                source, sid = parts[4], parts[5]
                if sid in gateway.deleted and gateway.receipts_410:
                    return self._answer(410, _deleted_body(sid))
                body = dict(
                    protocol_version=2, customer_id=CUSTOMER, source=source, session_id=sid,
                    state="deleted" if sid in gateway.deleted else "absent", receipts=[],
                )
                if sid in gateway.streams and sid not in gateway.deleted:
                    body.update(state="ready", stream=gateway.streams[sid])
                self._answer(200, body)

            def do_POST(self):
                raw = self.rfile.read(int(self.headers["Content-Length"]))
                gateway.requests.append(("POST", self.path, raw))
                data = json.loads(raw)
                sid = data["session_id"]
                if gateway.upload_answer is not None:
                    return self._answer(*gateway.upload_answer)
                if sid in gateway.deleted or sid in gateway.deleted_on_upload:
                    gateway.deleted.add(sid)
                    return self._answer(410, _deleted_body(sid))
                receipt = {
                    k: data[k]
                    for k in ("batch_seq", "source_byte_end", "source_line_end", "event_end",
                              "prefix_sha256")
                }
                receipt.update(body_sha256=hashlib.sha256(raw).hexdigest(),
                               finalized=bool(data.get("finalize")))
                gateway.streams[sid] = dict(receipt, stream_id=data["stream_id"],
                                            last_seq=data["batch_seq"])
                self._answer(202, {"status": "accepted", "protocol_version": 2,
                                   "receipt": receipt})

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def posts(self, sid: str) -> list[dict]:
        return [json.loads(raw) for method, _p, raw in self.requests
                if method == "POST" and json.loads(raw)["session_id"] == sid]


@pytest.fixture
def gateway():
    g = Gateway()
    yield g
    g.httpd.shutdown()
    g.httpd.server_close()


def _lane(census, gateway, tmp_path, **kwargs):
    stages = []
    outcome = bt.import_transcripts(
        census,
        poster=bt.Poster(gateway.url, "synthetic-token", timeout=5),
        device_id="",
        ledger=bt.TranscriptLedger(tmp_path / "ledger"),
        assignments={},
        on_stage=lambda done, total, transcript, phase: stages.append(phase),
        **kwargs,
    )
    return outcome, stages


def _journal_says_deleted(gateway, sid: str) -> bool:
    journal = Journal(gateway.url, CUSTOMER, "claude_code")
    try:
        return journal.is_deleted(sid)
    finally:
        journal.close()


def test_a_deleted_session_is_skipped_never_sent_and_never_a_failure(tmp_path, gateway):
    gone = _transcript(tmp_path, sid=str(uuid4()))
    fresh = _transcript(tmp_path, sid=str(uuid4()))
    gateway.deleted.add(gone.session_id)

    outcome, stages = _lane(bt.Census(candidates=[gone, fresh]), gateway, tmp_path)

    assert (outcome.skipped_deleted, outcome.failed, outcome.finalized) == (1, 0, 1)
    assert outcome.errors == [] and outcome.retryable_failures == 0
    assert gateway.posts(gone.session_id) == []
    assert gateway.posts(fresh.session_id), "the rest of the import is unaffected"
    assert _journal_says_deleted(gateway, gone.session_id), "final for the live tap too"
    assert "Deleted at your team's request; not uploaded" in stages
    assert "1 deleted at your team's request (not uploaded)" in "\n".join(outcome.lines())


def test_a_deletion_landing_mid_upload_is_final_and_recorded_for_the_tap(tmp_path, gateway):
    transcript = _transcript(tmp_path)
    gateway.deleted_on_upload.add(transcript.session_id)

    outcome, stages = _lane(bt.Census(candidates=[transcript]), gateway, tmp_path)

    assert (outcome.skipped_deleted, outcome.failed, outcome.pending_batches) == (1, 0, 0)
    assert len(gateway.posts(transcript.session_id)) == 1, "refused once, not retried"
    assert stages[-1] == "Deleted at your team's request; not uploaded"
    # The journal is the one the live tap reads (same state dir, same team).
    journal = Journal(gateway.url, CUSTOMER, "claude_code")
    assert journal.is_deleted(transcript.session_id)
    assert journal.pending(transcript.session_id) is None
    journal.close()

    # A second import asks once and sends nothing.
    before = len(gateway.requests)
    again, _ = _lane(bt.Census(candidates=[transcript]), gateway, tmp_path)
    assert again.skipped_deleted == 1 and again.failed == 0
    assert [r[0] for r in gateway.requests[before:]] == ["GET"]


def test_a_410_on_the_receipts_read_is_a_skip_too(tmp_path, gateway):
    transcript = _transcript(tmp_path)
    gateway.deleted.add(transcript.session_id)
    gateway.receipts_410 = True
    outcome, _ = _lane(bt.Census(candidates=[transcript]), gateway, tmp_path,
                       expected_customer_id=CUSTOMER)
    assert (outcome.skipped_deleted, outcome.failed) == (1, 0)
    assert gateway.posts(transcript.session_id) == []
    assert _journal_says_deleted(gateway, transcript.session_id)


@pytest.mark.parametrize(
    "body",
    [{"detail": "gone"}, {"detail": {"reason": "other"}}, _deleted_body(str(uuid4()))],
    ids=["string-detail", "other-reason", "another-session"],
)
def test_a_410_that_is_not_this_sessions_deletion_is_a_failure_and_keeps_it(
    tmp_path, gateway, body
):
    transcript = _transcript(tmp_path)
    gateway.upload_answer = (410, body)
    outcome, _ = _lane(bt.Census(candidates=[transcript]), gateway, tmp_path)
    assert (outcome.skipped_deleted, outcome.failed) == (0, 1)
    assert outcome.pending_batches == 1, "the batch is kept for a retry"
    assert not _journal_says_deleted(gateway, transcript.session_id)


def test_upload_session_reports_a_deleted_session_as_done_not_failed(tmp_path, gateway):
    transcript = _transcript(tmp_path)
    gateway.deleted.add(transcript.session_id)
    record = bt.SessionRecord(
        session_id=transcript.session_id, path=str(transcript.path), agent=transcript.agent
    )
    result = bt.upload_session(
        transcript, record, bt.Poster(gateway.url, "synthetic-token", timeout=5), device_id=""
    )
    assert result.ok and result.deleted and result.error is None and not result.retryable
    assert gateway.posts(transcript.session_id) == []
