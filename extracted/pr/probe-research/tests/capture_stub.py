"""A stub of the ingest routes the tap talks to, over real HTTP on 127.0.0.1.

The receipts read, the batch door (a batch continues its stream exactly where
the server's cursor ends, else 409), the session title and the ingestion
status. Protocol 2 by default; `IngestStub(protocol=3)` offers protocol 3 as
the real door does (`accepts`: protocols, fragment versions, no events), and
pins each stream to the protocol of its first batch. A stream it holds reads
`state: "ready"`, as the real door's does (the tap reconciles a finalized one
only then). It keeps every batch it took, so a test can say which transcript
lines reached the server and which never did. `delay_s` slows every batch
down; `refusing` answers `refusal_code` (503: a server that cannot take it
for now) to every batch. Stdlib only; one per test (`IngestStub.start`, then `stop`).
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CUSTOMER = "c-stub"
_RECEIPTS = re.compile(r"^/ingest/v1/sessions/([^/]+)/([^/?]+)/receipts")
_TITLE = re.compile(r"^/ingest/v1/sessions/([^/]+)/([^/]+)/title$")
_BATCH = re.compile(r"^/ingest/v1/sessions/([^/]+)$")
_SOURCES = {"claude-code": "claude_code", "codex": "codex", "pi": "pi", "kimi": "kimi"}


class IngestStub:
    def __init__(self, *, protocol: int = 2) -> None:
        self.protocol = protocol
        #: Seconds every batch waits before it is answered.
        self.delay_s = 0.0
        #: Answer `refusal_code` to every batch: 503, the server cannot take
        #: it for now; a 403 or 401 refuses it for good.
        self.refusing = False
        self.refusal_code = 503
        self.lock = threading.Lock()
        #: `{sid: stream}`, as the receipts read serves it.
        self.streams: dict[str, dict] = {}
        #: Every batch the door accepted: `(sid, payload)`.
        self.batches: list[tuple[str, dict]] = []
        #: Every request: `(method, path)`.
        self.requests: list[tuple[str, str]] = []
        stub = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args) -> None:  # quiet
                pass

            def _answer(self, code: int, body: dict) -> None:
                data = json.dumps(body).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self) -> None:  # noqa: N802
                with stub.lock:
                    stub.requests.append(("GET", self.path))
                if self.path.startswith("/ingest/v1/sessions/status"):
                    return self._answer(200, {"ingest_enabled": True})
                found = _RECEIPTS.match(self.path)
                if found:
                    source, sid = found.groups()
                    with stub.lock:
                        stream = dict(stub.streams[sid]) if sid in stub.streams else None
                    answer = {"protocol_version": (stream or {}).get("protocol_version", 2), "customer_id": CUSTOMER,
                              "source": source, "session_id": sid, "state": "ready" if stream else "absent"}
                    if stub.protocol == 3:
                        answer["accepts"] = {"protocols": [2, 3], "fragment_versions": [1, 2], "events": False}
                    if stream:
                        answer["stream"] = {k: v for k, v in stream.items() if k != "protocol_version"}
                    return self._answer(200, answer)
                return self._answer(404, {"detail": "not found"})

            def do_POST(self) -> None:  # noqa: N802
                body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                with stub.lock:
                    stub.requests.append(("POST", self.path))
                if _TITLE.match(self.path):
                    return self._answer(200, {"status": "ok"})
                found = _BATCH.match(self.path)
                if not found:
                    return self._answer(404, {"detail": "not found"})
                if stub.delay_s:
                    time.sleep(stub.delay_s)
                if stub.refusing:
                    return self._answer(stub.refusal_code, {"detail": "the ingest door is not taking batches now"})
                payload = json.loads(body)
                sid = payload["session_id"]
                protocol = payload.get("protocol_version")
                final = payload.get("finalize") is True  # a FINALIZE carries no events, no fragments
                if protocol == 3 and (stub.protocol != 3 or not (final or isinstance(payload.get("fragments"), list))):
                    return self._answer(422, {"detail": "protocol 3 batches carry fragments"})
                if protocol == 2 and not (final or isinstance(payload.get("events"), list)):
                    return self._answer(422, {"detail": "batches before protocol 3 carry events"})
                with stub.lock:
                    stream = stub.streams.get(sid)
                    if stream is not None and stream["protocol_version"] != protocol:
                        return self._answer(409, {"detail": "protocol mismatch"})
                    start = stream or {"last_seq": -1, "source_byte_end": 0, "source_line_end": 0, "event_end": 0}
                    if not (
                        payload["batch_seq"] == start["last_seq"] + 1
                        and payload["source_byte_start"] == start["source_byte_end"]
                        and payload["source_line_start"] == start["source_line_end"]
                        and payload["event_start"] == start["event_end"]
                    ):
                        return self._answer(409, {"detail": "batch does not continue the stream"})
                    stub.streams[sid] = {
                        "protocol_version": protocol,
                        "stream_id": payload["stream_id"], "last_seq": payload["batch_seq"],
                        "source_byte_end": payload["source_byte_end"], "source_line_end": payload["source_line_end"],
                        "event_end": payload["event_end"], "prefix_sha256": payload["prefix_sha256"],
                        "finalized": bool(payload.get("finalize")),
                    }
                    stub.batches.append((sid, payload))
                receipt = {k: payload[k] for k in ("batch_seq", "source_byte_end", "source_line_end", "event_end",
                                                   "prefix_sha256")}
                receipt.update(body_sha256=hashlib.sha256(body).hexdigest(), finalized=bool(payload.get("finalize")))
                return self._answer(202, {"protocol_version": protocol, "receipt": receipt})

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        host, port = self.server.server_address[:2]
        return f"http://{host}:{port}"

    def start(self) -> IngestStub:
        self.thread.start()
        return self

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()

    # -- what reached the server ---------------------------------------------------

    def sent_text(self, sid: str) -> str:
        """Everything the session's accepted batches carried, as one string."""
        with self.lock:
            return "\n".join(json.dumps(p, sort_keys=True) for s, p in self.batches if s == sid)

    def stream(self, sid: str) -> dict | None:
        with self.lock:
            return dict(self.streams[sid]) if sid in self.streams else None

    def asked_about(self, sid: str) -> list[tuple[str, str]]:
        """Every request that named the session (its receipts, its title)."""
        with self.lock:
            return [r for r in self.requests if sid in r[1]]
