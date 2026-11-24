from __future__ import annotations

import base64
import contextlib
import datetime
import functools
import http.client
import json
import os
import re
import sys
import threading
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

import requests
from requests.structures import CaseInsensitiveDict

from bitfab import service_calls, whole_objects
from bitfab.client_patching import PatchingFinder
from bitfab.github_sandbox import (
    GITHUB_SANDBOX_NAME,
    READ_WHOLE_OBJECT,
    REF_READ_TIMEOUT_SECONDS,
    TOKEN_ENV,
    PullSource,
    make_upstream,
    pull_target,
    read_pull_at_head,
    read_whole_pull,
    record_github_refs,
)
from bitfab.integration_fixture import (
    extract_integration_fixtures,
    has_integration_fixture,
)
from bitfab.sandbox import SANDBOX_FIXTURE_PREFIX

SESSIONS_MODULE = "requests.sessions"
PATCHED_MARKER = "_bitfab_github_patched"
INTEGRATION = "github"
GITHUB_API_HOSTS = frozenset({"api.github.com"})
MAX_RECORDED_BODY_BYTES = 1024 * 1024
RESULT_HEADERS = ("Content-Type", "Link")
SNAPSHOT_FIXTURE = f"{SANDBOX_FIXTURE_PREFIX}{GITHUB_SANDBOX_NAME}"
MAX_REMEMBERED_TRACES = 10_000
ANY_ACCEPT = "*/*"
PULL_HEAD = "pullHead"
WHOLE_PULL = "pull"
REPO_PREFIX = re.compile(r"^/repos/(?P<owner>[^/]+)/(?P<name>[^/]+)(?P<rest>/.*)?$")
REPO_ROUTES: tuple[tuple[str, str, str], ...] = (
    ("GET", r"", "github.repos.get"),
    ("GET", r"/contents(?:/.*)?", "github.contents.get"),
    ("PUT", r"/contents/.+", "github.contents.put"),
    ("DELETE", r"/contents/.+", "github.contents.delete"),
    ("GET", r"/readme(?:/.*)?", "github.readme.get"),
    ("GET", r"/git/trees/.+", "github.git.trees.get"),
    ("POST", r"/git/trees", "github.git.trees.create"),
    ("GET", r"/git/blobs/.+", "github.git.blobs.get"),
    ("POST", r"/git/blobs", "github.git.blobs.create"),
    ("GET", r"/git/commits/.+", "github.git.commits.get"),
    ("POST", r"/git/commits", "github.git.commits.create"),
    ("GET", r"/commits", "github.commits.list"),
    ("GET", r"/commits/.+?/statuses", "github.statuses.list"),
    ("GET", r"/commits/.+?/status", "github.status.get"),
    ("GET", r"/commits/.+?/check-runs", "github.checks.listForRef"),
    ("GET", r"/commits/.+", "github.commits.get"),
    ("GET", r"/compare/.+", "github.compare.get"),
    ("GET", r"/(?:tarball|zipball)(?:/.*)?", "github.archive.get"),
    ("GET", r"/branches", "github.branches.list"),
    ("GET", r"/branches/.+", "github.branches.get"),
    ("GET", r"/tags", "github.tags.list"),
    ("GET", r"/git/ref/.+", "github.git.refs.get"),
    ("GET", r"/git/(?:matching-refs|refs)(?:/.*)?", "github.git.refs.list"),
    ("POST", r"/git/refs", "github.git.refs.create"),
    ("PATCH", r"/git/refs/.+", "github.git.refs.update"),
    ("DELETE", r"/git/refs/.+", "github.git.refs.delete"),
    ("GET", r"/pulls", "github.pulls.list"),
    ("GET", r"/pulls/\d+(?:/.*)?", "github.pulls.get"),
    ("POST", r"/pulls", "github.pulls.create"),
    ("GET", r"/issues", "github.issues.list"),
    ("GET", r"/issues/\d+(?:/.*)?", "github.issues.get"),
    ("GET", r"/issues/comments/\d+", "github.issues.comments.get"),
    ("POST", r"/issues/\d+/comments", "github.issues.comments.create"),
    ("PATCH", r"/issues/comments/\d+", "github.issues.comments.update"),
    ("POST", r"/pulls/\d+/comments", "github.pulls.comments.create"),
    ("POST", r"/pulls/\d+/reviews", "github.pulls.reviews.create"),
    ("POST", r"/statuses/[0-9a-f]{40}", "github.statuses.create"),
    ("POST", r"/check-runs", "github.checks.create"),
    ("PATCH", r"/check-runs/\d+", "github.checks.update"),
    ("GET", r"/check-runs/\d+", "github.checks.get"),
)
TOP_ROUTES: tuple[tuple[str, str, str], ...] = (
    ("GET", r"/search/code", "github.search.code"),
    (
        "POST",
        r"/app/installations/[^/]+/access_tokens",
        "github.app.installation_token.create",
    ),
)
OTHER_OPERATION = "github.other"

_lock = threading.Lock()
_snapshot_tried: set[str] = set()
_recorded_states: dict[str, dict[str, Any]] = {}


def operation_name(method: str, path: str) -> str:
    verb = method.upper()
    found = REPO_PREFIX.match(path)
    routes, rest = (
        (REPO_ROUTES, found.group("rest") or "") if found else (TOP_ROUTES, path)
    )
    rest = rest.rstrip("/") if rest != "/" else ""
    return next(
        (
            name
            for route_verb, pattern, name in routes
            if route_verb == verb and re.fullmatch(pattern, rest)
        ),
        OTHER_OPERATION,
    )


def repo_of(path: str) -> str | None:
    found = REPO_PREFIX.match(path)
    return f"{found.group('owner')}/{found.group('name')}" if found else None


def _body(request: Any) -> Any:
    body = getattr(request, "body", None)
    if body is None or body in (b"", ""):
        return None
    if isinstance(body, bytes):
        with contextlib.suppress(UnicodeDecodeError):
            body = body.decode("utf-8")
    if isinstance(body, str):
        with contextlib.suppress(ValueError):
            return json.loads(body)
    return None


def _accept(request: Any) -> dict[str, str]:
    accept = str((getattr(request, "headers", None) or {}).get("Accept") or "")
    wants_other = accept and "json" not in accept and accept != "*/*"
    return {"accept": accept} if wants_other else {}


def request_params(request: Any) -> dict[str, Any]:
    parsed = urlsplit(request.url)
    query = {
        name: values[0] if len(values) == 1 else values
        for name, values in parse_qs(parsed.query, keep_blank_values=True).items()
    }
    return {
        "method": str(request.method or "GET").upper(),
        "path": parsed.path or "/",
        "query": query,
        "body": _body(request),
        "repo": repo_of(parsed.path or "/"),
        **_accept(request),
    }


def request_token(request: Any) -> str | None:
    header = str((getattr(request, "headers", None) or {}).get("Authorization") or "")
    scheme, _, value = header.partition(" ")
    if scheme.lower() in ("token", "bearer") and value:
        return value.strip()
    if scheme.lower() == "basic" and value:
        with contextlib.suppress(ValueError, UnicodeDecodeError):
            _, _, password = base64.b64decode(value).decode("utf-8").partition(":")
            return password or None
    return None


def _result_headers(response: Any) -> dict[str, str]:
    return {
        name: response.headers[name]
        for name in RESULT_HEADERS
        if name in response.headers
    }


def _size(response: Any) -> int | None:
    with contextlib.suppress(TypeError, ValueError):
        return int(response.headers.get("Content-Length"))
    return None


def response_result(response: Any, streamed: bool) -> dict[str, Any]:
    status = int(response.status_code)
    headers = _result_headers(response)
    omitted = {"status": status, "headers": headers, "bodyOmitted": True}
    if streamed:
        return {**omitted, "size": _size(response)}
    content = response.content or b""
    is_json = "json" in str(response.headers.get("Content-Type") or "").lower()
    if not content:
        return {"status": status, "headers": headers, "json": None}
    if not is_json or len(content) > MAX_RECORDED_BODY_BYTES:
        return {**omitted, "size": len(content)}
    try:
        return {"status": status, "headers": headers, "json": json.loads(content)}
    except ValueError:
        return {**omitted, "size": len(content)}


def _content(result: dict[str, Any]) -> bytes:
    if isinstance(result.get("file"), str):
        return Path(result["file"]).read_bytes()
    if result.get("json") is not None:
        return json.dumps(result["json"]).encode("utf-8")
    if isinstance(result.get("text"), str):
        return result["text"].encode("utf-8")
    return b""


def response_from_result(result: Any, request: Any) -> requests.Response:
    if not isinstance(result, dict) or not isinstance(result.get("status"), int):
        raise TypeError(
            "A GitHub call answered during replay must return "
            '{"status": int, "headers": {...}, "json": ...}; got '
            f"{type(result).__name__}."
        )
    response = requests.Response()
    response.status_code = result["status"]
    response.headers = CaseInsensitiveDict(result.get("headers") or {})
    if result.get("json") is not None and "Content-Type" not in response.headers:
        response.headers["Content-Type"] = "application/json; charset=utf-8"
    response._content = _content(result)
    response._content_consumed = True
    response.url = request.url
    response.request = request
    response.encoding = "utf-8"
    response.reason = http.client.responses.get(result["status"], "")
    response.elapsed = datetime.timedelta(0)
    return response


def _recording_client_present() -> bool:
    return any(
        service_calls._records(client, INTEGRATION)
        for client in service_calls._alive_clients()
    )


def _should_capture(repo: str | None) -> bool:
    if repo is None or service_calls.replaying():
        return False
    client = sys.modules.get("bitfab.client")
    if (
        client is None
        or not client._get_span_stack()
        or not _recording_client_present()
    ):
        return False
    root = client._trace_root_span_context()
    if root is None or has_integration_fixture(root, SNAPSHOT_FIXTURE):
        return False
    trace_id = str(root.get("traceId"))
    with _lock:
        if trace_id in _snapshot_tried:
            return False
        if len(_snapshot_tried) >= MAX_REMEMBERED_TRACES:
            _snapshot_tried.clear()
        _snapshot_tried.add(trace_id)
    return True


def capture_snapshot(repo: str | None, request: Any) -> None:
    with contextlib.suppress(Exception):
        if _should_capture(repo) and repo is not None:
            record_github_refs(
                [repo], token=request_token(request), _timeout=REF_READ_TIMEOUT_SECONDS
            )


def _read_whole_pull_for(params: dict[str, Any], request: Any) -> Any:
    repo = params.get("repo")
    found = REPO_PREFIX.match(str(params.get("path") or ""))
    if params.get("method") != "GET" or not isinstance(repo, str) or found is None:
        return None
    target = pull_target(
        found.group("rest") or "", request.headers.get("Accept") or ANY_ACCEPT
    )
    if target is None:
        return None
    source = PullSource(
        upstream=make_upstream(
            request_token(request) or os.environ.get(TOKEN_ENV), None, None
        ),
        name=repo,
        base=f"/repos/{repo}",
    )
    number, sha, _ = target
    if number is None:
        if not whole_objects.claim(PULL_HEAD, f"{repo}@{sha}"):
            return None
        number = read_pull_at_head(source, sha or "")
        if number is None:
            return None
    if not whole_objects.claim(WHOLE_PULL, f"{repo}#{number}"):
        return None
    return repo, number, read_whole_pull(source, number)


def save_whole_pull(params: dict[str, Any], request: Any) -> None:
    with contextlib.suppress(Exception):
        client = sys.modules.get("bitfab.client")
        root = client._trace_root_span_context() if client is not None else None
        if (
            root is None
            or service_calls.recording_mode(INTEGRATION) != READ_WHOLE_OBJECT
        ):
            return
        read = _read_whole_pull_for(params, request)
        if read is None:
            return
        repo, number, pull = read
        trace_id = str(root.get("traceId"))
        with _lock:
            if (
                trace_id not in _recorded_states
                and len(_recorded_states) >= MAX_REMEMBERED_TRACES
            ):
                _recorded_states.clear()
            state = _recorded_states.setdefault(trace_id, {"wholePulls": {}})
            state["wholePulls"].setdefault(repo, {})[number] = pull
            snapshot = (extract_integration_fixtures(root) or {}).get(SNAPSHOT_FIXTURE)
            saved = {**(snapshot if isinstance(snapshot, dict) else {}), **state}
        service_calls.save_recorded_sandbox_state(
            INTEGRATION, GITHUB_SANDBOX_NAME, trace_id, json.loads(json.dumps(saved))
        )


def _patched_send(original: Any) -> Any:
    @functools.wraps(original)
    def send(self: Any, request: Any, **kwargs: Any) -> Any:
        host = None
        with contextlib.suppress(Exception):
            host = urlsplit(request.url).hostname
        if host not in GITHUB_API_HOSTS or not service_calls.is_recorded(INTEGRATION):
            return original(self, request, **kwargs)
        params = request_params(request)
        capture_snapshot(params["repo"], request)
        save_whole_pull(params, request)
        held: list[Any] = []

        def send_to_github() -> dict[str, Any]:
            response = original(self, request, **kwargs)
            held.append(response)
            return response_result(response, bool(kwargs.get("stream")))

        result = service_calls.run(
            service_calls.ServiceCall(
                integration=INTEGRATION,
                method=operation_name(params["method"], params["path"]),
                params=params,
                send=send_to_github,
                request=request,
            )
        )
        if held:
            return held[-1]
        return response_from_result(result, request)

    setattr(send, PATCHED_MARKER, True)
    return send


def patch_module(module: Any) -> None:
    with _lock:
        if getattr(module, "__name__", "") != SESSIONS_MODULE:
            return
        cls = getattr(module, "Session", None)
        send = getattr(cls, "send", None)
        if cls is not None and send and not getattr(send, PATCHED_MARKER, False):
            cls.send = _patched_send(send)


_finder = PatchingFinder(lambda name: name == SESSIONS_MODULE, patch_module)


def install() -> None:
    _finder.install()
    module = sys.modules.get(SESSIONS_MODULE)
    if module is not None:
        with contextlib.suppress(Exception):
            patch_module(module)
