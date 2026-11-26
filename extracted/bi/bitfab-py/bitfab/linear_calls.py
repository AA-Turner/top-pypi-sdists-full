from __future__ import annotations

import contextlib
import copy
import functools
import http.client
import json
import sys
import threading
from collections.abc import Callable
from typing import Any
from urllib.parse import parse_qsl, urlsplit

import requests
from requests.structures import CaseInsensitiveDict

from bitfab import service_calls, whole_objects
from bitfab.client_patching import PatchingFinder
from bitfab.linear_sandbox import (
    ISSUE,
    LINEAR_INTEGRATION,
    LINEAR_SANDBOX_NAME,
    LINEAR_SPAN_PREFIX,
    LinearCallRefusedError,
    LinearRecording,
    issue_ids_created,
    issue_ids_read,
    issue_ids_written,
    operation_span_name,
    record_call,
    record_whole_issue,
)
from bitfab.linear_whole import run_reads, run_reads_async, whole_issue_reads
from bitfab.recorded_states import update_recorded_state
from bitfab.sandbox import current_session, fail_replay_item

SESSIONS_MODULE = "requests.sessions"
HTTPX_MODULE = "httpx"
PATCHED_MODULES = frozenset({SESSIONS_MODULE, HTTPX_MODULE})
PATCHED_MARKER = "_bitfab_linear_patched"
LINEAR_API_HOST = "api.linear.app"
GRAPHQL_PATH = "/graphql"
REQUEST_KEYS = ("query", "variables", "operationName")

_lock = threading.Lock()


def linear_sandbox_on() -> bool:
    session = current_session()
    return session is not None and session.find_named(LINEAR_SANDBOX_NAME) is not None


def _is_linear_host(host: str | None) -> bool:
    return host == LINEAR_API_HOST


def _parsed_json(body: Any) -> Any:
    if isinstance(body, (bytes, bytearray)):
        try:
            body = bytes(body).decode("utf-8")
        except UnicodeDecodeError:
            return None
    if not isinstance(body, str) or body == "":
        return None
    with contextlib.suppress(ValueError):
        return json.loads(body)
    return None


def graphql_params(url: str, body: Any) -> dict[str, Any]:
    parsed = _parsed_json(body)
    if not isinstance(parsed, dict):
        parsed = dict(parse_qsl(urlsplit(url).query))
        if isinstance(parsed.get("variables"), str):
            parsed["variables"] = _parsed_json(parsed["variables"])
    return {key: parsed[key] for key in REQUEST_KEYS if parsed.get(key) is not None}


def _refused(where: str) -> LinearCallRefusedError:
    refused = LinearCallRefusedError(
        f"A request to {where} was held back during replay so it never reaches "
        "Linear: the Linear sandbox is on, and it answers GraphQL requests to "
        f"{LINEAR_API_HOST}{GRAPHQL_PATH} made with requests or httpx only."
    )
    fail_replay_item(refused)
    return refused


def run_linear_call(params: dict[str, Any]) -> Any:
    session = current_session()
    client = getattr(session, "client", None)
    name = operation_span_name(params)
    if client is None:
        raise service_calls.ServiceCallHeldBackError(
            f"{name} was held back during replay: no Bitfab client is set up."
        )
    call = service_calls.ServiceCall(
        integration=LINEAR_INTEGRATION,
        method=name,
        params=params,
        send=lambda: None,
    )
    current = service_calls._current.set(call)
    try:
        return service_calls._traced_call(client, name)(**params)
    finally:
        service_calls._current.reset(current)


def _save_to_store(change: Callable[[LinearRecording], None]) -> None:
    client = service_calls.recording_client(LINEAR_INTEGRATION)
    trace_id = whole_objects.current_trace_id()
    if client is None or trace_id is None:
        return
    update_recorded_state(
        trace_id,
        LINEAR_SANDBOX_NAME,
        LinearRecording,
        change,
        lambda recording: copy.deepcopy(recording.state),
        lambda state, version: client.http_client.send_sandbox_store_write(
            trace_id, LINEAR_SANDBOX_NAME, state, version
        ),
    )


def _save_call(params: dict[str, Any], output: Any) -> None:
    _save_to_store(lambda recording: record_call(recording, params, output))


def _save_whole_issue(issue_id: str, output: Any) -> None:
    if output is not None:
        _save_to_store(
            lambda recording: record_whole_issue(recording, issue_id, output)
        )


def _capture_whole_issues(ids: list[str], fetch: Any) -> None:
    for issue_id in ids:
        _save_whole_issue(
            issue_id,
            whole_objects.capture(
                LINEAR_INTEGRATION,
                LINEAR_SPAN_PREFIX,
                ISSUE,
                issue_id,
                functools.partial(fetch, issue_id),
            ),
        )


def _skip_created(params: dict[str, Any], output: Any) -> None:
    for issue_id in issue_ids_created(params, output):
        whole_objects.claim(ISSUE, issue_id)


def record_linear_call(params: dict[str, Any], send: Any, fetch_whole: Any) -> Any:
    _capture_whole_issues(issue_ids_written(params), fetch_whole)
    output = service_calls.run(
        service_calls.ServiceCall(
            integration=LINEAR_INTEGRATION,
            method=operation_span_name(params),
            params=params,
            send=send,
        )
    )
    _save_call(params, output)
    _skip_created(params, output)
    _capture_whole_issues(issue_ids_read(params, output), fetch_whole)
    return output


def _should_record() -> bool:
    return not service_calls.replaying() and service_calls.is_recorded(
        LINEAR_INTEGRATION
    )


def _requests_response(answer: Any, request: Any) -> requests.Response:
    response = requests.Response()
    response.status_code = 200
    response.headers = CaseInsensitiveDict(
        {"Content-Type": "application/json; charset=utf-8"}
    )
    response._content = json.dumps(answer).encode("utf-8")
    response._content_consumed = True
    response.url = request.url
    response.request = request
    response.encoding = "utf-8"
    response.reason = "OK"
    return response


def _patched_send(original: Any) -> Any:
    @functools.wraps(original)
    def send(self: Any, request: Any, **kwargs: Any) -> Any:
        parsed = urlsplit(request.url)
        if not _is_linear_host(parsed.hostname):
            return original(self, request, **kwargs)
        if linear_sandbox_on():
            if parsed.path.rstrip("/") != GRAPHQL_PATH:
                raise _refused(f"{parsed.hostname}{parsed.path}")
            answer = run_linear_call(graphql_params(request.url, request.body))
            return _requests_response(answer, request)
        if parsed.path.rstrip("/") != GRAPHQL_PATH or not _should_record():
            return original(self, request, **kwargs)
        held: list[Any] = []

        def send_to_linear() -> Any:
            response = original(self, request, **kwargs)
            held.append(response)
            return _parsed_json(response.content)

        def send_whole(body: dict[str, Any]) -> Any:
            whole = request.copy()
            whole.prepare_body(data=None, files=None, json=body)
            return _parsed_json(original(self, whole, **kwargs).content)

        def fetch_whole(issue_id: str) -> Any:
            return run_reads(whole_issue_reads(issue_id), send_whole)

        record_linear_call(
            graphql_params(request.url, request.body), send_to_linear, fetch_whole
        )
        return held[-1]

    setattr(send, PATCHED_MARKER, True)
    return send


def _httpx_body(request: Any) -> Any:
    with contextlib.suppress(Exception):
        return request.content
    return None


def _httpx_response(module: Any, answer: Any, request: Any) -> Any:
    return module.Response(200, json=answer, request=request)


def _whole_httpx_request(client: Any, request: Any, body: dict[str, Any]) -> Any:
    headers = {
        name: value
        for name, value in request.headers.items()
        if name.lower() not in ("content-length", "content-type")
    }
    return client.build_request("POST", request.url, headers=headers, json=body)


def _patched_httpx_send(original: Any, module: Any) -> Any:
    @functools.wraps(original)
    def send(self: Any, request: Any, *args: Any, **kwargs: Any) -> Any:
        url = request.url
        if not _is_linear_host(url.host):
            return original(self, request, *args, **kwargs)
        if linear_sandbox_on():
            if url.path.rstrip("/") != GRAPHQL_PATH:
                raise _refused(f"{url.host}{url.path}")
            answer = run_linear_call(graphql_params(str(url), _httpx_body(request)))
            return _httpx_response(module, answer, request)
        if url.path.rstrip("/") != GRAPHQL_PATH or not _should_record():
            return original(self, request, *args, **kwargs)
        held: list[Any] = []

        def send_to_linear() -> Any:
            response = original(self, request, *args, **kwargs)
            response.read()
            held.append(response)
            return _parsed_json(response.content)

        def send_whole(body: dict[str, Any]) -> Any:
            response = original(self, _whole_httpx_request(self, request, body))
            response.read()
            return _parsed_json(response.content)

        def fetch_whole(issue_id: str) -> Any:
            return run_reads(whole_issue_reads(issue_id), send_whole)

        record_linear_call(
            graphql_params(str(url), _httpx_body(request)), send_to_linear, fetch_whole
        )
        return held[-1]

    setattr(send, PATCHED_MARKER, True)
    return send


async def _capture_whole_issues_async(ids: list[str], fetch: Any) -> None:
    for issue_id in ids:
        if not whole_objects.claim(ISSUE, issue_id):
            continue
        with contextlib.suppress(Exception):
            answer = await fetch(issue_id)
            _save_whole_issue(
                issue_id,
                whole_objects.record(
                    LINEAR_INTEGRATION,
                    LINEAR_SPAN_PREFIX,
                    ISSUE,
                    issue_id,
                    lambda answer=answer: answer,
                ),
            )


def _patched_httpx_async_send(original: Any, module: Any) -> Any:
    @functools.wraps(original)
    async def send(self: Any, request: Any, *args: Any, **kwargs: Any) -> Any:
        url = request.url
        if not _is_linear_host(url.host):
            return await original(self, request, *args, **kwargs)
        if linear_sandbox_on():
            if url.path.rstrip("/") != GRAPHQL_PATH:
                raise _refused(f"{url.host}{url.path}")
            answer = run_linear_call(graphql_params(str(url), _httpx_body(request)))
            return _httpx_response(module, answer, request)
        if url.path.rstrip("/") != GRAPHQL_PATH or not _should_record():
            return await original(self, request, *args, **kwargs)

        async def send_whole(body: dict[str, Any]) -> Any:
            response = await original(self, _whole_httpx_request(self, request, body))
            await response.aread()
            return _parsed_json(response.content)

        async def fetch_whole(issue_id: str) -> Any:
            return await run_reads_async(whole_issue_reads(issue_id), send_whole)

        params = graphql_params(str(url), _httpx_body(request))
        await _capture_whole_issues_async(issue_ids_written(params), fetch_whole)
        response = await original(self, request, *args, **kwargs)
        await response.aread()
        output = service_calls.run(
            service_calls.ServiceCall(
                integration=LINEAR_INTEGRATION,
                method=operation_span_name(params),
                params=params,
                send=lambda: _parsed_json(response.content),
            )
        )
        _save_call(params, output)
        _skip_created(params, output)
        await _capture_whole_issues_async(issue_ids_read(params, output), fetch_whole)
        return response

    setattr(send, PATCHED_MARKER, True)
    return send


def _patched_putrequest(original: Any) -> Any:
    @functools.wraps(original)
    def putrequest(self: Any, method: str, url: str, *args: Any, **kwargs: Any) -> Any:
        host = getattr(self, "host", None)
        if _is_linear_host(host) and linear_sandbox_on():
            raise _refused(f"{host}{urlsplit(url).path or url}")
        return original(self, method, url, *args, **kwargs)

    setattr(putrequest, PATCHED_MARKER, True)
    return putrequest


def _patch_method(cls: Any, name: str, wrap: Any) -> None:
    original = getattr(cls, name, None)
    if original is not None and not getattr(original, PATCHED_MARKER, False):
        setattr(cls, name, wrap(original))


def patch_module(module: Any) -> None:
    name = getattr(module, "__name__", "")
    with _lock:
        if name == SESSIONS_MODULE:
            _patch_method(getattr(module, "Session", None), "send", _patched_send)
        elif name == HTTPX_MODULE:
            _patch_method(
                getattr(module, "Client", None),
                "send",
                lambda original: _patched_httpx_send(original, module),
            )
            _patch_method(
                getattr(module, "AsyncClient", None),
                "send",
                lambda original: _patched_httpx_async_send(original, module),
            )


_finder = PatchingFinder(lambda name: name in PATCHED_MODULES, patch_module)


def install() -> None:
    _finder.install()
    with _lock:
        _patch_method(http.client.HTTPConnection, "putrequest", _patched_putrequest)
    for name in PATCHED_MODULES:
        module = sys.modules.get(name)
        if module is not None:
            with contextlib.suppress(Exception):
                patch_module(module)
