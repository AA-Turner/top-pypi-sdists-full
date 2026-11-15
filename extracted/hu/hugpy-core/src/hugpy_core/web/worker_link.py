"""Workers Core cannot open a connection to: their Wrapper connects out to Core, and Core suggests over that link.

Operator 2026-11-14: "the wrapper operates on host authority", "core is supposed to suggest", "the wrapper can
receive a core delegation". A box on another network (a-brain, behind its own router) reaches Core the way it
reaches hugpy.ai to download; Core does not reach it. So the Wrapper holds the link open and Core puts what it
would have sent on it:

  GET  /fleet-link/install.sh           the worker installer, open (the console's + Worker line fetches it)
  POST /fleet-link/register             a Core "use" key (the install line's) -> this worker's link secret. Core saves
                                        the worker with the internal address below and the secret as its key.
  GET  /fleet-link/<name>/poll?wait=25  (the Wrapper, Bearer <secret>) the requests Core has for it, waiting for one
  POST /fleet-link/<name>/answer        (the Wrapper, Bearer <secret>) {id, status, content_type, body_b64}
  POST /fleet-link/<name>/answer/<id>   (the Wrapper, Bearer <secret>) the answer streamed: its raw bytes, with
                                        X-Hugpy-Status and X-Hugpy-Content-Type; piped block by block to the
                                        request waiting for it (2026-11-15: no base64, no JSON, no whole buffer)
  ANY  /_link/<name>/<path>             (Core's own code, Bearer <secret>) one request to the Wrapper over the link:
                                        it is queued for the poll and its answer returned as the Wrapper gave it.

Every part of Core that calls a Wrapper (intake's health and telemetry reads, calls, cancel, settings) uses the
saved address and key as they are, so a linked worker is called exactly like one Core reaches directly. The
Wrapper sends each request to its own front door, where its own admission, templates and queue decide: Core
suggests, the host decides. A long answer (a stream) arrives whole when it is done.

This is a WSGI door outermost in Core's chain (web/app.py), before the console's gates: its routes carry their own
credential. The link state is this process's memory: Core's web service is one process (werkzeug, threaded).
"""
from __future__ import annotations

import base64
import hmac
import json
import os
import queue
import secrets
import threading
import time
import uuid

STREAM_BLOCK = 1 << 20
STREAM_STALL_S = 600          # a streamed answer whose reader stops taking blocks this long is abandoned

LINK_PREFIX = "/_link/"
FLEET_PREFIX = "/fleet-link/"
POLL_WAIT_S = 25          # the Wrapper's poll is held this long when Core has nothing for it
ALIVE_S = 75              # a link not polled for this long is down: a request on it fails at once
ANSWER_WAIT_S = 3600      # a request waits at most this long for its answer
MAX_BATCH = 16
NAME_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
PASSED_HEADERS = ("Content-Type", "Accept")


class _Link:
    def __init__(self):
        self.cond = threading.Condition()
        self.pending = []           # requests not yet taken by a poll
        self.waiting = {}           # id -> [Event, answer or None]
        self.last_poll = 0.0


_LINKS: dict = {}
_LOCK = threading.Lock()


def _link(name):
    with _LOCK:
        return _LINKS.setdefault(name, _Link())


def internal_base():
    """Where Core's other services (intake, its own web code) reach this process."""
    return (os.environ.get("HUGPY_CORE_LINK_BASE") or f"http://127.0.0.1:{os.environ.get('HUGPY_CORE_PORT') or 7020}").rstrip("/")


def internal_url(name):
    return internal_base() + LINK_PREFIX.rstrip("/") + "/" + name


def connected(name):
    return time.time() - _link(name).last_poll < ALIVE_S


def suggest(name, method, path, content_type, body, *, timeout=ANSWER_WAIT_S):
    """One request to ``name``'s Wrapper over its link -> (status, content_type, body bytes)."""
    link = _link(name)
    if not connected(name):
        ago = f"{time.time() - link.last_poll:.0f} s ago" if link.last_poll else "not since Core started"
        raise LookupError(f"{name}'s Wrapper has not polled Core for its link ({ago}): is hugpy-wrapper running there?")
    job = dict(id=uuid.uuid4().hex, method=method, path=path, content_type=content_type,
               body_b64=base64.b64encode(body or b"").decode())
    slot = [threading.Event(), None]
    with link.cond:
        link.waiting[job["id"]] = slot
        link.pending.append(job)
        link.cond.notify_all()
    deadline = time.time() + timeout
    try:
        while not slot[0].wait(5):
            if time.time() > deadline:
                raise TimeoutError(f"{name}'s Wrapper did not answer {method} {path} in {timeout} s")
            if not connected(name):
                raise LookupError(f"{name}'s Wrapper stopped polling Core while {method} {path} was on its link")
        return slot[1]
    finally:
        with link.cond:
            link.waiting.pop(job["id"], None)
            if job in link.pending:
                link.pending.remove(job)


def take(name, wait=POLL_WAIT_S):
    """The Wrapper's poll: the requests waiting for it (up to MAX_BATCH), held up to ``wait`` s for one."""
    link = _link(name)
    link.last_poll = time.time()
    with link.cond:
        if not link.pending:
            link.cond.wait(max(0.0, min(float(wait), 55.0)))
        jobs, link.pending[:] = link.pending[:MAX_BATCH], link.pending[MAX_BATCH:]
    link.last_poll = time.time()
    return jobs


def answer(name, job_id, status, content_type, body):
    link = _link(name)
    with link.cond:
        slot = link.waiting.get(job_id)
    if slot is None:
        return False            # its caller gave up (timed out) or Core restarted
    slot[1] = (int(status), content_type or "application/json", body)
    slot[0].set()
    return True


# ---------------------------------------------------------------------------------------------- registration

def _secret_ok(name, environ):
    from hugpy_core.registry import registrations
    said = environ.get("HTTP_AUTHORIZATION") or ""
    given = said[7:].strip() if said[:7].lower() == "bearer " else ""
    worker = registrations.get(name)
    secret = (worker or {}).get("key") or ""
    return bool(worker and worker.get("link") and given and secret
                and hmac.compare_digest(given.encode(), secret.encode()))


def register(environ, body):
    """POST /fleet-link/register, Bearer <a Core use key>: {name} -> {name, secret, poll, answer}."""
    from hugpy_core.registry import registrations
    from hugpy_core.web.api_access import valid_use_authorization
    if not valid_use_authorization(environ.get("HTTP_AUTHORIZATION") or ""):
        return 401, {"error": "a valid Core API key is required (the install line's --core-key)"}
    name = str((body or {}).get("name") or "").strip()
    if not name or not set(name) <= NAME_CHARS:
        return 400, {"error": "name: letters, digits, dot, underscore or dash"}
    existing = registrations.get(name)
    if existing and not existing.get("link"):
        from hugpy_core.web.worker_connect import _still_answers_as
        if _still_answers_as(existing, name):
            return 409, {"error": f"{name} is connected directly at {existing['url']} and answers there: give this "
                                  f"box its own name (\"worker\" in /etc/hugpy/wrapper/settings.json)"}
    secret = "hlk_" + secrets.token_urlsafe(32)
    saved = registrations.upsert({"name": name, "url": internal_url(name), "key": secret, "link": True,
                                  "link_registered_at": time.time()})
    if not registrations.is_connected(saved):
        registrations.set_connected(name, True)
    return 200, {"name": name, "secret": secret, "poll": f"{FLEET_PREFIX}{name}/poll",
                 "answer": f"{FLEET_PREFIX}{name}/answer", "state": "linked",
                 "message": "Linked: this Wrapper polls Core for its work; its telemetry appears as intake refreshes."}


# ---------------------------------------------------------------------------------------------- WSGI door

def _read(environ, limit=1 << 31):
    try:
        size = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        size = 0
    return environ["wsgi.input"].read(min(size, limit)) if size > 0 else b""


def _json(start_response, status, obj):
    data = json.dumps(obj).encode()
    start_response(f"{status} {'OK' if status < 400 else 'Error'}",
                   [("Content-Type", "application/json"), ("Content-Length", str(len(data))), ("Cache-Control", "no-store")])
    return [data]


class WorkerLinkDoor:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO") or "/"
        if path.startswith(FLEET_PREFIX):
            return self._fleet(environ, start_response, path[len(FLEET_PREFIX):])
        if path.startswith(LINK_PREFIX):
            return self._forward(environ, start_response, path[len(LINK_PREFIX):])
        return self.app(environ, start_response)

    def _fleet(self, environ, start_response, rest):
        method = environ.get("REQUEST_METHOD")
        if rest == "install.sh" and method in ("GET", "HEAD"):
            return self._installer(start_response)
        if rest.startswith("relay/") and method == "GET":
            return self._relay(environ, start_response, rest[len("relay/"):])
        if rest == "register" and method == "POST":
            try:
                body = json.loads(_read(environ, 1 << 16) or b"{}")
            except ValueError:
                return _json(start_response, 400, {"error": "expected a JSON object"})
            status, doc = register(environ, body if isinstance(body, dict) else {})
            return _json(start_response, status, doc)
        name, _, leaf = rest.partition("/")
        if leaf.startswith("answer/") and method == "POST":
            if not _secret_ok(name, environ):
                return _json(start_response, 401, {"error": f"not {name}'s link secret"})
            return self._answer_stream(environ, start_response, name, leaf[len("answer/"):])
        if not name or leaf not in ("poll", "answer"):
            return _json(start_response, 404, {"error": "no such link route"})
        if not _secret_ok(name, environ):
            return _json(start_response, 401, {"error": f"not {name}'s link secret: register again "
                                                        f"(sudo hugpy-wrapper system register --core ... --link)"})
        if leaf == "poll" and method == "GET":
            from urllib.parse import parse_qs
            wait = (parse_qs(environ.get("QUERY_STRING") or "").get("wait") or [POLL_WAIT_S])[0]
            try:
                wait = float(wait)
            except ValueError:
                wait = POLL_WAIT_S
            return _json(start_response, 200, {"jobs": take(name, wait)})
        if leaf == "answer" and method == "POST":
            try:
                doc = json.loads(_read(environ))
                ok = answer(name, doc["id"], doc["status"], doc.get("content_type"),
                            base64.b64decode(doc.get("body_b64") or ""))
            except (ValueError, KeyError, TypeError) as exc:
                return _json(start_response, 400, {"error": f"an answer is {{id, status, content_type, body_b64}}: {exc}"})
            return _json(start_response, 200, {"taken": ok})
        return _json(start_response, 405, {"error": "poll is GET, answer is POST"})

    def _relay(self, environ, start_response, rest):
        """GET /fleet-link/relay/<token>/file?rel=&offset=&length=: a range of a file of the one model the token names,
        from its holder (registry/fleet_central.py). The token is the credential, for that copy only."""
        from urllib.parse import parse_qs
        from hugpy_core.registry import fleet_central
        token, _, leaf = rest.partition("/")
        said = environ.get("HTTP_AUTHORIZATION") or ""
        claims = fleet_central.verify(token)
        if claims is None or leaf != "file" or said[7:].strip() != token:
            return _json(start_response, 401, {"error": "not a live relay token for this copy"})
        q = {k: v[0] for k, v in parse_qs(environ.get("QUERY_STRING") or "").items()}
        try:
            status, data = fleet_central.relay_range(claims, q.get("rel", ""), int(q.get("offset") or 0),
                                                     int(q.get("length") or 0))
        except (ValueError, OSError) as exc:
            return _json(start_response, 502, {"error": f"the holder {claims['h']} did not answer: {exc}"})
        start_response(f"{status} Relayed", [("Content-Type", "application/octet-stream" if status == 200 else
                                              "application/json"), ("Content-Length", str(len(data))),
                                             ("Cache-Control", "no-store")])
        return [data]

    def _installer(self, start_response):
        """GET /fleet-link/install.sh: the worker installer (web/install.sh) with CENTRAL = this Core's public base
        (HUGPY_SELF_BASE). Open: it holds no secret (the key is on the command line the operator copies), and a new
        box has no console login, which /api/fleet/workers/install.sh is behind at the front."""
        import re
        import shlex
        from hugpy_core.imports.functions import self_base
        path = os.environ.get("HUGPY_CORE_WORKER_BOOTSTRAP") or os.path.join(os.path.dirname(__file__), "install.sh")
        try:
            with open(path, encoding="utf-8") as fh:
                script = fh.read()
            base = self_base().rstrip("/")
            if not re.fullmatch(r"https?://[A-Za-z0-9._:-]+", base):
                raise ValueError(f"HUGPY_SELF_BASE is not an origin: {base!r}")
        except (OSError, ValueError) as exc:
            data, status = f"echo 'worker installer unavailable: {exc}' >&2; exit 1\n".encode(), "503 Unavailable"
        else:
            data, status = re.sub(r"^CENTRAL=.*$", "CENTRAL=" + shlex.quote(base), script, count=1,
                                  flags=re.M).encode(), "200 OK"
        start_response(status, [("Content-Type", "text/x-shellscript"), ("Content-Length", str(len(data))),
                                ("Cache-Control", "no-store")])
        return [data]

    def _answer_stream(self, environ, start_response, name, job_id):
        """The Wrapper's streamed answer: its bytes go to the waiting request as they arrive."""
        link = _link(name)
        with link.cond:
            slot = link.waiting.get(job_id)
        if slot is None:
            return _json(start_response, 404, {"error": "no request is waiting for this answer (it timed out?)"})
        try:
            length = int(environ.get("CONTENT_LENGTH") or 0)
            status = int(environ.get("HTTP_X_HUGPY_STATUS") or 200)
        except ValueError:
            return _json(start_response, 400, {"error": "a streamed answer has Content-Length and X-Hugpy-Status"})
        pipe = queue.Queue(maxsize=16)
        slot[1] = ("stream", status, environ.get("HTTP_X_HUGPY_CONTENT_TYPE") or "application/json", length, pipe)
        slot[0].set()
        stream, left = environ["wsgi.input"], length
        try:
            while left > 0:
                block = stream.read(min(STREAM_BLOCK, left))
                if not block:
                    break
                pipe.put(block, timeout=STREAM_STALL_S)
                left -= len(block)
            pipe.put(None, timeout=STREAM_STALL_S)
        except queue.Full:
            return _json(start_response, 504, {"error": "the request waiting for this answer stopped reading"})
        return _json(start_response, 200, {"taken": left == 0})

    def _forward(self, environ, start_response, rest):
        name, _, tail = rest.partition("/")
        if not name or not _secret_ok(name, environ):
            return _json(start_response, 401, {"error": "not this worker's link key"})
        target = "/" + tail
        if environ.get("QUERY_STRING"):
            target += "?" + environ["QUERY_STRING"]
        try:
            answer_ = suggest(name, environ.get("REQUEST_METHOD") or "GET", target,
                              environ.get("CONTENT_TYPE") or "", _read(environ))
        except LookupError as exc:
            return _json(start_response, 502, {"error": str(exc), "source": "link"})
        except TimeoutError as exc:
            return _json(start_response, 504, {"error": str(exc), "source": "link"})
        if answer_[0] == "stream":                     # the Wrapper streams it: piped through as it comes
            _, status, ctype, length, pipe = answer_
            start_response(f"{status} Linked", [("Content-Type", ctype), ("Content-Length", str(length)),
                                                ("Cache-Control", "no-store")])

            def blocks():
                while True:
                    block = pipe.get(timeout=STREAM_STALL_S)
                    if block is None:
                        return
                    yield block
            return blocks()
        status, ctype, body = answer_
        start_response(f"{status} Linked", [("Content-Type", ctype), ("Content-Length", str(len(body))),
                                            ("Cache-Control", "no-store")])
        return [body]


def wrap(app):
    return WorkerLinkDoor(app)
