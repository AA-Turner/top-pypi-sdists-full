from __future__ import annotations

import asyncio
import contextlib
import functools
import http.client
import json
import sys
import threading
from email.parser import BytesParser
from email.policy import HTTP
from typing import Any
from urllib.parse import parse_qsl, urlsplit

import requests
from requests.structures import CaseInsensitiveDict

from bitfab import service_calls
from bitfab.client_patching import PatchingFinder
from bitfab.sandbox import current_session, fail_replay_item
from bitfab.slack_sandbox import (
    READ_REAL_WRITE_FAKE,
    RECORDED,
    SLACK_INTEGRATION,
    SLACK_SANDBOX_NAME,
    SLACK_SPAN_PREFIX,
    WEBHOOK_METHOD,
    SlackCallAccess,
    SlackCallRefusedError,
    reading_slack,
)

SYNC_CLIENT_MODULE = "slack_sdk.web.base_client"
ASYNC_CLIENT_MODULE = "slack_sdk.web.async_base_client"
SESSIONS_MODULE = "requests.sessions"
SYNC_WEBHOOK_MODULE = "slack_sdk.webhook.client"
ASYNC_WEBHOOK_MODULE = "slack_sdk.webhook.async_client"
PATCHED_MODULES = frozenset(
    {
        SYNC_CLIENT_MODULE,
        ASYNC_CLIENT_MODULE,
        SESSIONS_MODULE,
        SYNC_WEBHOOK_MODULE,
        ASYNC_WEBHOOK_MODULE,
    }
)
PATCHED_MARKER = "_bitfab_slack_patched"
API_PATH = "/api/"
UPLOAD_HOST = "files.slack.com"
UPLOAD_PATH = "/upload/"
HOOKS_HOST = "hooks.slack.com"
SECRET_KEYS = frozenset(
    {
        "access_token",
        "refresh_token",
        "token",
        "client_secret",
        "bot_access_token",
        "id_token",
    }
)
SECRET_HOLDERS = {
    "authed_user": SECRET_KEYS,
    "bot": SECRET_KEYS,
    "incoming_webhook": SECRET_KEYS | {"url"},
}
DOWNLOAD_HTTP_METHODS = frozenset({"GET", "HEAD"})

_lock = threading.Lock()


def _slack_sandbox() -> Any:
    session = current_session()
    return session.find_named(SLACK_SANDBOX_NAME) if session is not None else None


def slack_sandbox_on() -> bool:
    return _slack_sandbox() is not None


def _is_file_download(host: str | None, path: str, http_method: str) -> bool:
    return (
        host == UPLOAD_HOST
        and not path.startswith(UPLOAD_PATH)
        and http_method.upper() in DOWNLOAD_HTTP_METHODS
    )


def _download_passes(host: str | None, path: str, http_method: str) -> bool:
    if not _is_file_download(host, path, http_method):
        return False
    sandbox = _slack_sandbox()
    if sandbox is not None and sandbox.mode == RECORDED:
        refused = SlackCallRefusedError(
            f"A download of {host}{path} was held back during replay: the Slack "
            f"sandbox runs in {RECORDED} mode, and the original trace recorded "
            "no file contents to answer it with. Replay with "
            f'sandbox_modes={{"slack": "{READ_REAL_WRITE_FAKE}"}} to download '
            "the real file."
        )
        fail_replay_item(refused)
        raise refused
    return True


def _is_slack_host(host: str | None) -> bool:
    return host == "slack.com" or bool(host and host.endswith(".slack.com"))


def _bearer(headers: Any) -> str | None:
    header = str((headers or {}).get("Authorization") or "")
    scheme, _, value = header.partition(" ")
    return value.strip() if scheme.lower() == "bearer" and value.strip() else None


def run_slack_call(
    method: str, params: dict[str, Any], access: SlackCallAccess
) -> dict[str, Any]:
    session = current_session()
    client = getattr(session, "client", None)
    if client is None:
        raise service_calls.ServiceCallHeldBackError(
            f"{method} was held back during replay: no Bitfab client is set up."
        )
    given = {name: value for name, value in params.items() if value is not None}
    token = given.get("token") or access.token
    sent = _without_secrets(given)
    name = f"{SLACK_SPAN_PREFIX}{method}"
    call = service_calls.ServiceCall(
        integration=SLACK_INTEGRATION,
        method=name,
        params=sent,
        send=lambda: None,
        request=SlackCallAccess(token=token, api_url=access.api_url),
    )
    current = service_calls._current.set(call)
    try:
        return service_calls._traced_call(client, name)(**sent)
    finally:
        service_calls._current.reset(current)


def _parsed_body(body: Any) -> Any:
    if isinstance(body, (bytes, bytearray)):
        body = body.decode("utf-8", "replace")
    if isinstance(body, str):
        with contextlib.suppress(ValueError):
            return json.loads(body)
        return None
    return body if isinstance(body, dict) else None


def _without_secrets(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    kept = {name: item for name, item in value.items() if name not in SECRET_KEYS}
    for holder, secrets in SECRET_HOLDERS.items():
        if isinstance(kept.get(holder), dict):
            kept[holder] = {
                name: item for name, item in kept[holder].items() if name not in secrets
            }
    return kept


def record_slack_call(
    method: str,
    params: dict[str, Any],
    access: SlackCallAccess,
    send: Any,
) -> Any:
    sent = _without_secrets(
        {name: value for name, value in params.items() if value is not None}
    )
    answered: list[Any] = []

    def send_and_scrub() -> Any:
        answer = send()
        answered.append(answer)
        return _without_secrets(answer)

    result = service_calls.run(
        service_calls.ServiceCall(
            integration=SLACK_INTEGRATION,
            method=f"{SLACK_SPAN_PREFIX}{method}",
            params=sent,
            send=send_and_scrub,
            request=access,
        )
    )
    return answered[-1] if answered else result


def _client_access(client: Any, args: dict[str, Any]) -> SlackCallAccess:
    return SlackCallAccess(
        token=_bearer(args.get("headers")) or getattr(client, "token", None),
        api_url=getattr(client, "base_url", None),
    )


def _method_of(url: str, base_url: str | None) -> str | None:
    address = url.split("?", 1)[0]
    if base_url and address.startswith(base_url):
        return address[len(base_url) :]
    return None


def _client_params(args: dict[str, Any]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for name in ("params", "data", "json"):
        if isinstance(args.get(name), dict):
            params.update(args[name])
    return {
        name: value
        for name, value in params.items()
        if isinstance(value, (str, int, float, bool, list, dict))
    }


def _client_answer(
    client: Any, url: str, args: dict[str, Any]
) -> dict[str, Any] | None:
    method = _method_of(url, getattr(client, "base_url", None))
    if method is None:
        return None
    return run_slack_call(method, _client_params(args), _client_access(client, args))


def _recorded_sync_request(
    original: Any, client: Any, url: str, args: dict[str, Any]
) -> Any:
    method = _method_of(url, getattr(client, "base_url", None))
    if method is None:
        return original(client, url=url, args=args)
    held: list[Any] = []

    def send() -> Any:
        response = original(client, url=url, args=args)
        held.append(response)
        return _parsed_body(
            response.get("body") if isinstance(response, dict) else None
        )

    record_slack_call(method, _client_params(args), _client_access(client, args), send)
    return held[-1]


def _patched_sync_request(original: Any) -> Any:
    @functools.wraps(original)
    def perform(self: Any, *, url: str, args: dict[str, Any]) -> dict[str, Any]:
        if not slack_sandbox_on():
            if service_calls.replaying() or not service_calls.is_recorded(
                SLACK_INTEGRATION
            ):
                return original(self, url=url, args=args)
            return _recorded_sync_request(original, self, url, args)
        answer = _client_answer(self, url, args)
        return {
            "status": 200,
            "headers": {},
            "body": json.dumps(answer or {"ok": True}),
        }

    setattr(perform, PATCHED_MARKER, True)
    return perform


def _patched_sync_upload(original: Any, result_type: Any) -> Any:
    @functools.wraps(original)
    def upload(self: Any, **kwargs: Any) -> Any:
        if not slack_sandbox_on():
            return original(self, **kwargs)
        return result_type(status=200, body="OK")

    setattr(upload, PATCHED_MARKER, True)
    return upload


def _patched_async_request(original: Any) -> Any:
    @functools.wraps(original)
    async def request(
        self: Any, *, http_verb: str, api_url: str, req_args: dict[str, Any]
    ) -> dict[str, Any]:
        if not slack_sandbox_on():
            response = await original(
                self, http_verb=http_verb, api_url=api_url, req_args=req_args
            )
            method = _method_of(api_url, getattr(self, "base_url", None))
            if (
                method is not None
                and not service_calls.replaying()
                and service_calls.is_recorded(SLACK_INTEGRATION)
            ):
                answered = response.get("data") if isinstance(response, dict) else None
                record_slack_call(
                    method,
                    _client_params(req_args),
                    _client_access(self, req_args),
                    lambda: answered,
                )
            return response
        answer = await asyncio.to_thread(_client_answer, self, api_url, req_args)
        return {"data": answer or {"ok": True}, "headers": {}, "status_code": 200}

    setattr(request, PATCHED_MARKER, True)
    return request


def _patched_async_upload(original: Any, result_type: Any) -> Any:
    @functools.wraps(original)
    async def upload(self: Any, **kwargs: Any) -> Any:
        if not slack_sandbox_on():
            return await original(self, **kwargs)
        return result_type(status=200, body="OK")

    setattr(upload, PATCHED_MARKER, True)
    return upload


def _patch_method(cls: Any, name: str, wrap: Any) -> None:
    original = getattr(cls, name, None)
    if original is not None and not getattr(original, PATCHED_MARKER, False):
        setattr(cls, name, wrap(original))


def _request_params(request: Any) -> dict[str, Any]:
    params: dict[str, Any] = dict(
        parse_qsl(urlsplit(request.url).query, keep_blank_values=True)
    )
    body = getattr(request, "body", None)
    content_type = str((request.headers or {}).get("Content-Type") or "")
    if "multipart/form-data" in content_type.lower():
        if isinstance(body, str):
            body = body.encode("utf-8")
        if isinstance(body, bytes):
            params.update(_multipart_fields(body, content_type))
        return params
    if isinstance(body, bytes):
        with contextlib.suppress(UnicodeDecodeError):
            body = body.decode("utf-8")
    if not isinstance(body, str) or body == "":
        return params
    content_type = content_type.lower()
    if "json" in content_type:
        with contextlib.suppress(ValueError):
            parsed = json.loads(body)
            if isinstance(parsed, dict):
                params.update(parsed)
        return params
    params.update(parse_qsl(body, keep_blank_values=True))
    return params


def _multipart_fields(body: bytes, content_type: str) -> dict[str, str]:
    message = BytesParser(policy=HTTP).parsebytes(
        f"Content-Type: {content_type}\r\n\r\n".encode() + body
    )
    if not message.is_multipart():
        return {}
    fields: dict[str, str] = {}
    for part in message.iter_parts():
        name = part.get_param("name", header="content-disposition")
        if not isinstance(name, str) or part.get_filename() is not None:
            continue
        content = part.get_payload(decode=True)
        if isinstance(content, bytes):
            fields[name] = _decoded_text(content, part.get_content_charset())
    return fields


def _decoded_text(content: bytes, charset: str | None) -> str:
    try:
        return content.decode(charset or "utf-8", "replace")
    except LookupError:
        return content.decode("utf-8", "replace")


def _requests_response(answer: dict[str, Any], request: Any) -> requests.Response:
    return _plain_response(
        json.dumps(answer), "application/json; charset=utf-8", request
    )


def _plain_response(content: str, content_type: str, request: Any) -> requests.Response:
    response = requests.Response()
    response.status_code = 200
    response.headers = CaseInsensitiveDict({"Content-Type": content_type})
    response._content = content.encode("utf-8")
    response._content_consumed = True
    response.url = request.url
    response.request = request
    response.encoding = "utf-8"
    response.reason = "OK"
    return response


def _patched_send(original: Any) -> Any:
    @functools.wraps(original)
    def send(self: Any, request: Any, **kwargs: Any) -> Any:
        if reading_slack.get():
            return original(self, request, **kwargs)
        parsed = urlsplit(request.url)
        if not _is_slack_host(parsed.hostname):
            return original(self, request, **kwargs)
        if not parsed.path.startswith(API_PATH):
            if not slack_sandbox_on() or _download_passes(
                parsed.hostname, parsed.path, str(request.method or "GET")
            ):
                return original(self, request, **kwargs)
            return _outside_api_answer(request)
        access = SlackCallAccess(
            token=_bearer(request.headers),
            api_url=f"{parsed.scheme}://{parsed.netloc}{API_PATH}",
        )
        method = parsed.path[len(API_PATH) :]
        if not slack_sandbox_on():
            if service_calls.replaying() or not service_calls.is_recorded(
                SLACK_INTEGRATION
            ):
                return original(self, request, **kwargs)
            held: list[Any] = []

            def send_to_slack() -> Any:
                response = original(self, request, **kwargs)
                held.append(response)
                return _parsed_body(response.content)

            record_slack_call(method, _request_params(request), access, send_to_slack)
            return held[-1]
        answer = run_slack_call(method, _request_params(request), access)
        return _requests_response(answer, request)

    setattr(send, PATCHED_MARKER, True)
    return send


def _outside_api_answer(request: Any) -> requests.Response:
    parsed = urlsplit(request.url)
    body, content_type = _outside_api(
        parsed.hostname, parsed.path, lambda: _request_params(request)
    )
    return _plain_response(body, content_type, request)


def _outside_api(host: str | None, path: str, params: Any) -> tuple[str, str]:
    if host == UPLOAD_HOST and path.startswith(UPLOAD_PATH):
        return "OK", "text/plain; charset=utf-8"
    if host == HOOKS_HOST:
        hook = path.strip("/").split("/", 1)[0]
        run_slack_call(
            WEBHOOK_METHOD,
            {**params(), "hook": hook},
            SlackCallAccess(),
        )
        return "ok", "text/html"
    refused = SlackCallRefusedError(
        f"A request to {host}{path} was held back during "
        "replay so it never reaches Slack: the Slack sandbox is on, and it "
        "answers Slack's Web API, incoming webhooks, response_url posts, and "
        "its own file upload addresses only."
    )
    fail_replay_item(refused)
    raise refused


def _webhook_answer(url: str, body: Any) -> tuple[str, str]:
    parsed = urlsplit(url)
    return _outside_api(
        parsed.hostname,
        parsed.path,
        lambda: dict(body) if isinstance(body, dict) else {},
    )


def _patched_webhook(original: Any, response_type: Any) -> Any:
    @functools.wraps(original)
    def perform(self: Any, *, body: Any, headers: Any) -> Any:
        url = str(getattr(self, "url", "") or "")
        if not slack_sandbox_on() or not _is_slack_host(urlsplit(url).hostname):
            return original(self, body=body, headers=headers)
        answer, content_type = _webhook_answer(url, body)
        return response_type(
            url=url,
            status_code=200,
            body=answer,
            headers={"Content-Type": content_type},
        )

    setattr(perform, PATCHED_MARKER, True)
    return perform


def _patched_async_webhook(original: Any, response_type: Any) -> Any:
    @functools.wraps(original)
    async def perform(self: Any, *, body: Any, headers: Any) -> Any:
        url = str(getattr(self, "url", "") or "")
        if not slack_sandbox_on() or not _is_slack_host(urlsplit(url).hostname):
            return await original(self, body=body, headers=headers)
        answer, content_type = await asyncio.to_thread(_webhook_answer, url, body)
        return response_type(
            url=url,
            status_code=200,
            body=answer,
            headers={"Content-Type": content_type},
        )

    setattr(perform, PATCHED_MARKER, True)
    return perform


def _patched_putrequest(original: Any) -> Any:
    @functools.wraps(original)
    def putrequest(self: Any, method: str, url: str, *args: Any, **kwargs: Any) -> Any:
        host = getattr(self, "host", None)
        if (
            _is_slack_host(host)
            and not reading_slack.get()
            and slack_sandbox_on()
            and not _download_passes(host, urlsplit(url).path, method)
        ):
            refused = SlackCallRefusedError(
                f"{getattr(self, 'host', '')}{urlsplit(url).path} was held back during "
                "replay so it never reaches Slack: the Slack sandbox is on, and "
                "this call was made by a Slack client the SDK does not answer "
                "for. It answers slack_sdk's WebClient and AsyncWebClient, and "
                "requests."
            )
            fail_replay_item(refused)
            raise refused
        return original(self, method, url, *args, **kwargs)

    setattr(putrequest, PATCHED_MARKER, True)
    return putrequest


def patch_module(module: Any) -> None:
    name = getattr(module, "__name__", "")
    with _lock:
        if name == SYNC_CLIENT_MODULE:
            cls = getattr(module, "BaseClient", None)
            result_type = getattr(module, "FileUploadV2Result", None)
            _patch_method(cls, "_perform_urllib_http_request", _patched_sync_request)
            _patch_method(
                cls, "_upload_file", lambda o: _patched_sync_upload(o, result_type)
            )
        elif name == ASYNC_CLIENT_MODULE:
            cls = getattr(module, "AsyncBaseClient", None)
            result_type = getattr(module, "FileUploadV2Result", None)
            _patch_method(cls, "_request", _patched_async_request)
            _patch_method(
                cls, "_upload_file", lambda o: _patched_async_upload(o, result_type)
            )
        elif name == SESSIONS_MODULE:
            _patch_method(getattr(module, "Session", None), "send", _patched_send)
        elif name == SYNC_WEBHOOK_MODULE:
            response_type = getattr(module, "WebhookResponse", None)
            _patch_method(
                getattr(module, "WebhookClient", None),
                "_perform_http_request",
                lambda o: _patched_webhook(o, response_type),
            )
        elif name == ASYNC_WEBHOOK_MODULE:
            response_type = getattr(module, "WebhookResponse", None)
            _patch_method(
                getattr(module, "AsyncWebhookClient", None),
                "_perform_http_request",
                lambda o: _patched_async_webhook(o, response_type),
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
