"""A local stand-in for Capy's public API (https://docs.capy.ai/api-reference).

Serves the read routes `probe capy` uses, from in-memory data, over real HTTP on
127.0.0.1, with Capy's documented shapes: pages are `{items, cursor}`. Thread
lists take `cursor` (`<epochMillis>:<id>`); subagent lists take `after` (the
last subagent's id). Message lists take `after`, an exclusive EVENT-ID cursor of
exactly 26 characters (a 400 otherwise), never a message id: a tool entry's id
is its tool call id. A message page's cursor is the last event it served, null
once no newer events remain, and UNCHANGED (equal to `after`) while unsettled
messages block paging (`unsettled_from`). Errors are tagged JSON: 401 for a bad
key, 404 for anything out of reach, 429 with a `Retry-After` header. Every
request is logged with its method (`methods`), so a test can prove reads only.

Used by the unit tests and by the model-free smoke (point PROBE_CAPY_API_BASE
at `.base`).
"""

from __future__ import annotations

import hashlib
import json
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

KEY = "capy_" + "t" * 43
ME = "user_me"
TEAMMATE = "user_mate"


def thread(tid: str, *, project: str = "proj_1", author: str = ME, status: str = "idle",
           activity: str = "2026-10-12T10:00:00Z", archived: bool = False) -> dict:
    return {
        "id": tid, "projectId": project, "authorId": author, "previousAuthorId": None,
        "title": f"Thread {tid}", "titleCustom": False, "status": status, "archived": archived,
        "lastModelId": None, "pullRequestAuthor": None, "usage": {},
        "createdAt": "2026-10-12T09:00:00Z", "updatedAt": activity, "lastActivityAt": activity,
        "hasUnreads": False, "mentionCount": 0, "owed": False, "member": True,
        "personal": False, "visibility": "org",
    }


def event_id(key: str, index: int) -> str:
    """The event id of the `index`th entry of a transcript: 26 characters,
    unique per transcript and position (entries are only ever appended)."""
    return (f"01EV{index:08d}" + hashlib.sha1(key.encode()).hexdigest())[:26].upper()


def message(mid: str, source: str, text: str, **extra) -> dict:
    return {"id": mid, "source": source, "text": text, "createdAt": "2026-10-12T09:30:00Z", **extra}


class FakeCapy:
    def __init__(self, page_size: int = 2) -> None:
        self.key = KEY
        self.page_size = page_size
        self.users = [
            {"id": ME, "email": "me@lab.example", "firstName": "Me", "lastName": "R"},
            {"id": TEAMMATE, "email": "mate@lab.example", "firstName": "Mate", "lastName": "R"},
        ]
        self.projects = [{"id": "proj_1", "name": "ml-research"}, {"id": "proj_2", "name": "infra"}]
        self.threads: dict[str, list[dict]] = {"proj_1": [], "proj_2": []}
        self.messages: dict[str, list[dict]] = {}
        self.subagents: dict[str, list[dict]] = {}
        self.subagent_messages: dict[str, list[dict]] = {}
        #: path -> list of status codes to answer before serving normally.
        self.fail: dict[str, list[int]] = {}
        #: transcript id -> index of its first unsettled entry (hidden, blocks paging).
        self.unsettled_from: dict[str, int] = {}
        self.requests: list[str] = []
        self.methods: list[str] = []
        self._server: ThreadingHTTPServer | None = None

    # -- data ---------------------------------------------------------------
    def add_thread(self, t: dict, messages: list[dict] | None = None) -> None:
        self.threads.setdefault(t["projectId"], []).append(t)
        self.messages.setdefault(t["id"], []).extend(messages or [])

    def add_subagent(self, tid: str, sid: str, messages: list[dict], status: str = "working") -> None:
        self.subagents.setdefault(tid, []).append(
            {"id": sid, "threadId": tid, "parentId": None, "subagentPath": "1", "projectId": "proj_1",
             "title": f"Subagent {sid}", "status": status, "usage": {}, "archived": False,
             "createdAt": "2026-10-12T09:40:00Z", "updatedAt": "2026-10-12T09:41:00Z"}
        )
        self.subagent_messages[sid] = list(messages)

    # -- server -------------------------------------------------------------
    @property
    def base(self) -> str:
        assert self._server is not None
        return f"http://127.0.0.1:{self._server.server_address[1]}/api/v1"

    def __enter__(self) -> FakeCapy:
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):  # quiet
                pass

            def do_GET(self):  # noqa: N802
                fake._handle(self)

            def _refuse(self):
                fake.methods.append(self.command)
                fake.requests.append(self.path)
                fake._send(self, 405, {"_tag": "capy/MethodNotAllowed"})

            do_POST = do_PUT = do_PATCH = do_DELETE = _refuse  # noqa: N815

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self._server.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *exc) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()

    # -- routing ------------------------------------------------------------
    def _send(self, handler, code: int, body: dict, headers: dict | None = None) -> None:
        data = json.dumps(body).encode()
        handler.send_response(code)
        handler.send_header("Content-Type", "application/json")
        for k, v in (headers or {}).items():
            handler.send_header(k, v)
        handler.send_header("Content-Length", str(len(data)))
        handler.end_headers()
        handler.wfile.write(data)

    def _limit(self, query: dict) -> int:
        return min(int((query.get("limit") or [self.page_size])[0]), self.page_size)

    def _page_after(self, items: list[dict], query: dict) -> dict:
        """Subagent lists: `after` is the last item's id."""
        after = (query.get("after") or [None])[0]
        limit = self._limit(query)
        start = 0
        if after:
            ids = [m["id"] for m in items]
            start = ids.index(after) + 1 if after in ids else len(items)
        page = items[start:start + limit]
        more = start + limit < len(items)
        return {"items": page, "cursor": page[-1]["id"] if more and page else None}

    def _page_events(self, key: str, items: list[dict], query: dict) -> tuple[int, dict]:
        """Message lists: `after` is an event id; see the module docstring."""
        after = (query.get("after") or [None])[0]
        if after is not None and len(after) != 26:
            return 400, {"_tag": "capy/BadRequest", "message": "after must be 26 characters"}
        events = [event_id(key, i) for i in range(len(items))]
        start = 0
        if after:
            start = events.index(after) + 1 if after in events else len(items)
        settled = self.unsettled_from.get(key, len(items))
        end = min(start + self._limit(query), settled, len(items))
        page = items[start:end] if end > start else []
        if end < settled:
            cursor = events[end - 1]
        elif settled < len(items):
            cursor = events[end - 1] if page else after
        else:
            cursor = None
        return 200, {"items": page, "cursor": cursor}

    def _handle(self, handler) -> None:
        parsed = urllib.parse.urlparse(handler.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        self.requests.append(handler.path)
        self.methods.append(handler.command)
        if handler.headers.get("Authorization") != f"Bearer {self.key}":
            return self._send(handler, 401, {"_tag": "capy/Unauthorized"})
        queued = self.fail.get(path)
        if queued:
            code = queued.pop(0)
            return self._send(handler, code, {"_tag": "capy/RateLimited" if code == 429 else "capy/Error"},
                              {"Retry-After": "1"} if code == 429 else None)
        if not path.startswith("/api/v1/"):
            return self._send(handler, 404, {"_tag": "capy/NotFound"})
        parts = path[len("/api/v1/"):].split("/")
        if parts == ["users"]:
            return self._send(handler, 200, {"items": self.users})
        if parts == ["projects"]:
            return self._send(handler, 200, {"items": self.projects})
        if parts == ["threads"]:
            project = (query.get("projectId") or [""])[0]
            if project not in self.threads:
                return self._send(handler, 404, {"_tag": "capy/ProjectNotFound"})
            items = self.threads[project]
            cursor = (query.get("cursor") or [""])[0]
            start = 0
            if cursor:
                ids = [t["id"] for t in items]
                last = cursor.split(":", 1)[1]
                start = ids.index(last) + 1 if last in ids else len(items)
            page = items[start:start + self._limit(query)]
            more = start + len(page) < len(items)
            return self._send(handler, 200, {
                "items": page, "cursor": f"1791000000000:{page[-1]['id']}" if more and page else None,
            })
        if len(parts) == 3 and parts[0] == "threads" and parts[2] == "messages":
            if parts[1] not in self.messages:
                return self._send(handler, 404, {"_tag": "capy/ThreadNotFound"})
            return self._send(handler, *self._page_events(parts[1], self.messages[parts[1]], query))
        if len(parts) == 3 and parts[0] == "threads" and parts[2] == "subagents":
            return self._send(handler, 200, self._page_after(self.subagents.get(parts[1], []), query))
        if len(parts) == 3 and parts[0] == "subagents" and parts[2] == "messages":
            if parts[1] not in self.subagent_messages:
                return self._send(handler, 404, {"_tag": "capy/SubagentNotFound"})
            return self._send(handler, *self._page_events(parts[1], self.subagent_messages[parts[1]], query))
        return self._send(handler, 404, {"_tag": "capy/NotFound"})
