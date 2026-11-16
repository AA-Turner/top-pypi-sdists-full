from __future__ import annotations

import contextlib
import datetime
import functools
import hashlib
import json
import re
import sys
import threading
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from bitfab import service_calls
from bitfab.client_patching import PatchingFinder

HTTP_MODULE = "googleapiclient.http"
CREDENTIALS_MODULE = "google.oauth2.credentials"
PATCHED_MARKER = "_bitfab_google_patched"
HTTP_ERROR_KEY = "__bitfabHttpError"
REPLAY_TOKEN = "bitfab-replay-token"
SERVICES = {"gmail": ("gmail", "Gmail")}
EXECUTE_PARAMS = ("http", "num_retries")
HELD_SCOPE_PREFIXES = (
    "https://www.googleapis.com/auth/gmail.",
    "https://mail.google.com/",
)
IDENTITY_SCOPES = frozenset(
    {
        "openid",
        "email",
        "profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    }
)
_PATH_PREFIX = re.compile(r"^/?(?:upload/)?(?P<service>[a-z0-9]+)/(?P<version>v[^/]+)/")
_TEMPLATE_PARAM = re.compile(r"\{\+?([A-Za-z0-9_]+)\}")

_lock = threading.Lock()
_methods: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
CREDENTIAL_PARAM = "credential"


def request_credentials(request: Any = None) -> Any:
    current = service_calls.current_call()
    chosen = request if request is not None else getattr(current, "request", None)
    http = getattr(chosen, "http", None)
    return getattr(http, "credentials", None)


def credential_fingerprint(credentials: Any) -> str | None:
    secret = getattr(credentials, "refresh_token", None) or getattr(
        credentials, "token", None
    )
    if not isinstance(secret, str) or not secret or secret == REPLAY_TOKEN:
        return None
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()[:16]


def _walk_methods(resource: dict[str, Any], into: dict[str, dict[str, Any]]) -> None:
    for method in (resource.get("methods") or {}).values():
        if isinstance(method, dict) and method.get("id"):
            into[method["id"]] = method
    for child in (resource.get("resources") or {}).values():
        if isinstance(child, dict):
            _walk_methods(child, into)


def _methods_for(service: str, version: str) -> dict[str, dict[str, Any]]:
    key = (service, version)
    if key in _methods:
        return _methods[key]
    found: dict[str, dict[str, Any]] = {}
    with contextlib.suppress(Exception):
        from_cache = sys.modules.get("googleapiclient.discovery_cache")
        if from_cache is None:
            __import__("googleapiclient.discovery_cache")
            from_cache = sys.modules["googleapiclient.discovery_cache"]
        document = from_cache.get_static_doc(service, version)
        if document:
            _walk_methods(json.loads(document), found)
    _methods[key] = found
    return found


def _path_params(template: str, path: str) -> dict[str, str]:
    pattern = (
        "^/?"
        + _TEMPLATE_PARAM.sub(
            lambda match: (
                f"(?P<{match.group(1)}>.+)"
                if template[match.start() + 1] == "+"
                else f"(?P<{match.group(1)}>[^/]+)"
            ),
            re.escape(template)
            .replace(r"\{", "{")
            .replace(r"\}", "}")
            .replace(r"\+", "+"),
        )
        + "$"
    )
    matched = re.match(pattern, path.removeprefix("/upload"))
    if matched is None:
        return {}
    return {name: unquote(value) for name, value in matched.groupdict().items()}


def _body(request: Any) -> Any:
    body = getattr(request, "body", None)
    if body is None or body == "":
        return None
    if isinstance(body, bytes):
        with contextlib.suppress(UnicodeDecodeError):
            body = body.decode("utf-8")
    if isinstance(body, str):
        with contextlib.suppress(ValueError):
            return json.loads(body)
    return body


def request_params(request: Any) -> tuple[str, str, dict[str, Any]] | None:
    method_id = getattr(request, "methodId", None)
    uri = getattr(request, "uri", None)
    if not isinstance(method_id, str) or not isinstance(uri, str):
        return None
    prefix = method_id.split(".", 1)[0]
    if prefix not in SERVICES:
        return None
    parsed = urlparse(uri)
    found = _PATH_PREFIX.match(parsed.path)
    method = (
        _methods_for(found.group("service"), found.group("version")).get(method_id)
        if found
        else None
    ) or {}
    declared = method.get("parameters") or {}
    params: dict[str, Any] = dict(_path_params(method.get("path") or "", parsed.path))
    for name, values in parse_qs(parsed.query).items():
        if name in {"alt", "prettyPrint"}:
            continue
        repeated = (declared.get(name) or {}).get("repeated", False)
        params[name] = values if repeated else values[-1]
    body = _body(request)
    if body is not None:
        params["body"] = body
    return method_id, prefix, params


def http_error(request: Any, error: dict[str, Any]) -> Exception:
    from_errors = sys.modules.get("googleapiclient.errors")
    httplib2 = sys.modules.get("httplib2")
    status = int(error.get("code") or 500)
    content = json.dumps({"error": error}).encode("utf-8")
    if from_errors is None or httplib2 is None:
        return RuntimeError(f"Google API error {status}: {error.get('message')}")
    response = httplib2.Response({"status": status})
    response.reason = error.get("status") or ""
    return from_errors.HttpError(response, content, uri=getattr(request, "uri", None))


def _patched_execute(original: Any) -> Any:
    @functools.wraps(original)
    def execute(self: Any, *args: Any, **kwargs: Any) -> Any:
        parsed = None
        with contextlib.suppress(Exception):
            parsed = request_params(self)
        if parsed is None or len(args) > len(EXECUTE_PARAMS):
            return original(self, *args, **kwargs)
        kwargs = {**dict(zip(EXECUTE_PARAMS, args)), **kwargs}
        args = ()
        method_id, prefix, params = parsed
        fingerprint = credential_fingerprint(request_credentials(self))
        if fingerprint is not None:
            params[CREDENTIAL_PARAM] = fingerprint
        result = service_calls.run(
            service_calls.ServiceCall(
                integration=SERVICES[prefix][0],
                method=method_id,
                params=params,
                send=lambda: original(self, *args, **kwargs),
                request=self,
            )
        )
        if isinstance(result, dict) and isinstance(result.get(HTTP_ERROR_KEY), dict):
            raise http_error(self, result[HTTP_ERROR_KEY])
        return result

    setattr(execute, PATCHED_MARKER, True)
    return execute


def only_held_scopes(credentials: Any) -> bool:
    scopes = getattr(credentials, "granted_scopes", None) or getattr(
        credentials, "scopes", None
    )
    if not scopes:
        return False
    if isinstance(scopes, str):
        scopes = scopes.split()
    api_scopes = [s for s in scopes if s not in IDENTITY_SCOPES]
    return bool(api_scopes) and all(
        s.startswith(HELD_SCOPE_PREFIXES) for s in api_scopes
    )


def _patched_refresh(original: Any) -> Any:
    @functools.wraps(original)
    def refresh(self: Any, request: Any) -> Any:
        if not service_calls.replaying() or not only_held_scopes(self):
            return original(self, request)
        self.token = REPLAY_TOKEN
        self.expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        return None

    setattr(refresh, PATCHED_MARKER, True)
    return refresh


def patch_module(module: Any) -> None:
    with _lock:
        if getattr(module, "__name__", "") == HTTP_MODULE:
            cls = getattr(module, "HttpRequest", None)
            execute = getattr(cls, "execute", None)
            if (
                cls is not None
                and execute
                and not getattr(execute, PATCHED_MARKER, False)
            ):
                cls.execute = _patched_execute(execute)
        if getattr(module, "__name__", "") == CREDENTIALS_MODULE:
            cls = getattr(module, "Credentials", None)
            refresh = getattr(cls, "refresh", None)
            if (
                cls is not None
                and refresh
                and not getattr(refresh, PATCHED_MARKER, False)
            ):
                cls.refresh = _patched_refresh(refresh)


_finder = PatchingFinder(
    lambda name: name in {HTTP_MODULE, CREDENTIALS_MODULE}, patch_module
)


def install() -> None:
    _finder.install()
    for name in (HTTP_MODULE, CREDENTIALS_MODULE):
        module = sys.modules.get(name)
        if module is not None:
            with contextlib.suppress(Exception):
                patch_module(module)
