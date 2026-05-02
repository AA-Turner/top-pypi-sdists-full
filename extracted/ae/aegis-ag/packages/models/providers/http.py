"""Shared JSON-over-HTTP execution helpers for provider adapters."""

from __future__ import annotations

from dataclasses import dataclass
from html import unescape as html_unescape
import json
import re
import shutil
import subprocess
from typing import Any, Mapping, Protocol, runtime_checkable
from urllib import error, request


DEFAULT_PROVIDER_HTTP_TIMEOUT_SECONDS = 10 * 60


@dataclass(frozen=True, slots=True)
class JSONHTTPResponse:
    status_code: int
    headers: Mapping[str, str]
    payload: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class JSONHTTPStreamChunk:
    event: str | None
    payload: Mapping[str, Any]


@runtime_checkable
class JSONHTTPTransport(Protocol):
    def post_json(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
    ) -> JSONHTTPResponse:
        """Send a JSON POST request and return the decoded JSON body."""

    def post_json_stream(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
    ):
        """Send a JSON POST request and yield decoded SSE payloads."""


class UrllibJSONHTTPTransport:
    """Standard-library JSON transport for deterministic local and live use."""

    def __init__(
        self,
        *,
        timeout_seconds: float = DEFAULT_PROVIDER_HTTP_TIMEOUT_SECONDS,
    ) -> None:
        self.timeout_seconds = timeout_seconds

    def post_json(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
    ) -> JSONHTTPResponse:
        body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        request_headers = dict(headers)
        request_headers.setdefault("Content-Type", "application/json")
        http_request = request.Request(
            url,
            data=body,
            headers=request_headers,
            method="POST",
        )
        try:
            with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                raw_body = response.read().decode("utf-8")
                parsed = json.loads(raw_body) if raw_body else {}
                if not isinstance(parsed, dict):
                    raise RuntimeError("provider response must be a JSON object")
                return JSONHTTPResponse(
                    status_code=response.status,
                    headers={str(key).lower(): str(value) for key, value in response.headers.items()},
                    payload=parsed,
                )
        except error.HTTPError as exc:  # pragma: no cover - exercised by callers
            message = self._error_message(exc, url=url)
            raise RuntimeError(message) from exc
        except error.URLError as exc:  # pragma: no cover - exercised by callers
            if self._should_retry_with_curl(exc):
                return self._post_json_with_curl(
                    url=url,
                    headers=request_headers,
                    body=body,
                )
            raise RuntimeError(f"provider request failed for {url}: {exc.reason}") from exc

    def _error_message(self, exc: error.HTTPError, *, url: str | None = None) -> str:
        try:
            body = exc.read().decode("utf-8", errors="replace").strip()
        except Exception:  # pragma: no cover - defensive fallback
            body = ""
        return self._status_error_message(
            status_code=int(exc.code),
            body=body,
            url=url or getattr(exc, "url", None),
        )

    def _status_error_message(
        self,
        *,
        status_code: int,
        body: str,
        url: str | None = None,
    ) -> str:
        detail = self._summarize_error_body(body)
        hint = self._provider_error_hint(status_code=status_code, url=url)
        parts = [f"provider request failed with status {status_code}."]
        if detail:
            parts.append(detail)
        if hint:
            parts.append(hint)
        return " ".join(part.strip() for part in parts if part.strip()).strip()

    def _summarize_error_body(self, body: str) -> str:
        trimmed = body.strip()
        if not trimmed:
            return ""
        try:
            parsed = json.loads(trimmed)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, Mapping):
            for path in (
                ("error", "message"),
                ("message",),
                ("error",),
                ("detail",),
            ):
                value: Any = parsed
                for key in path:
                    if not isinstance(value, Mapping):
                        value = None
                        break
                    value = value.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()[:200]
        lowered = trimmed.lower()
        if "<html" in lowered or "<body" in lowered:
            without_scripts = re.sub(r"(?is)<(script|style)\b.*?>.*?</\1>", " ", trimmed)
            text = re.sub(r"(?is)<[^>]+>", " ", without_scripts)
            text = re.sub(r"\s+", " ", html_unescape(text)).strip()
            if text:
                return f"Upstream returned an HTML error page instead of JSON: {text[:160]}"
            return "Upstream returned an HTML error page instead of JSON."
        return trimmed[:200]

    def _provider_error_hint(self, *, status_code: int, url: str | None) -> str:
        if status_code not in {401, 403}:
            return ""
        normalized_url = str(url or "").strip().lower()
        if "chatgpt.com/backend-api/codex" in normalized_url:
            return (
                "For openai-codex this can mean the session token is invalid, or that Aegis is hitting the "
                "wrong Codex backend path. Verify the provider is using `/responses` on `chatgpt.com/backend-api/codex`, "
                "then re-authenticate Codex only if the endpoint is already correct."
            )
        return ""

    def _should_retry_with_curl(self, exc: error.URLError) -> bool:
        reason_text = str(exc.reason)
        retryable_tls_fragments = (
            "WRONG_VERSION_NUMBER",
            "UNEXPECTED_EOF_WHILE_READING",
        )
        return any(fragment in reason_text for fragment in retryable_tls_fragments)

    def _post_json_with_curl(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        body: bytes,
    ) -> JSONHTTPResponse:
        curl = shutil.which("curl")
        if curl is None:
            raise RuntimeError(
                f"provider request failed for {url}: curl is unavailable for TLS fallback"
            )
        status_marker = "__AEGIS_STATUS__:"
        max_time = max(1, int(round(self.timeout_seconds)))
        connect_timeout = max(1, min(10, max_time))
        command = [
            curl,
            "--silent",
            "--show-error",
            "--location",
            "--connect-timeout",
            str(connect_timeout),
            "--max-time",
            str(max_time),
            "--request",
            "POST",
            url,
            "--data-binary",
            "@-",
            "--write-out",
            f"\n{status_marker}%{{http_code}}",
        ]
        for key, value in headers.items():
            command.extend(["--header", f"{key}: {value}"])
        result = subprocess.run(
            command,
            input=body,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            stderr = result.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"provider request failed for {url}: {stderr or 'curl fallback failed'}")
        raw_output = result.stdout.decode("utf-8", errors="replace")
        raw_body, separator, raw_status = raw_output.rpartition(f"\n{status_marker}")
        if not separator:
            raise RuntimeError(f"provider request failed for {url}: curl fallback missing status marker")
        try:
            status_code = int(raw_status.strip())
        except ValueError as exc:  # pragma: no cover - defensive fallback
            raise RuntimeError(f"provider request failed for {url}: invalid curl status marker") from exc
        payload = json.loads(raw_body) if raw_body else {}
        if not isinstance(payload, dict):
            raise RuntimeError("provider response must be a JSON object")
        if status_code >= 400:
            raise RuntimeError(
                self._status_error_message(
                    status_code=status_code,
                    body=raw_body,
                    url=url,
                )
            )
        return JSONHTTPResponse(
            status_code=status_code,
            headers={},
            payload=payload,
        )

    def _post_json_stream_with_curl(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        body: bytes,
    ):
        curl = shutil.which("curl")
        if curl is None:
            raise RuntimeError(
                f"provider request failed for {url}: curl is unavailable for TLS fallback"
            )
        status_marker = "__AEGIS_STATUS__:"
        max_time = max(1, int(round(self.timeout_seconds)))
        connect_timeout = max(1, min(10, max_time))
        command = [
            curl,
            "--silent",
            "--show-error",
            "--location",
            "--connect-timeout",
            str(connect_timeout),
            "--max-time",
            str(max_time),
            "--request",
            "POST",
            url,
            "--data-binary",
            "@-",
            "--write-out",
            f"\n{status_marker}%{{http_code}}",
        ]
        for key, value in headers.items():
            command.extend(["--header", f"{key}: {value}"])
        result = subprocess.run(
            command,
            input=body,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            stderr = result.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"provider request failed for {url}: {stderr or 'curl fallback failed'}")
        raw_output = result.stdout.decode("utf-8", errors="replace")
        raw_body, separator, raw_status = raw_output.rpartition(f"\n{status_marker}")
        if not separator:
            raise RuntimeError(f"provider request failed for {url}: curl fallback missing status marker")
        try:
            status_code = int(raw_status.strip())
        except ValueError as exc:  # pragma: no cover - defensive fallback
            raise RuntimeError(f"provider request failed for {url}: invalid curl status marker") from exc
        if status_code >= 400:
            raise RuntimeError(
                self._status_error_message(
                    status_code=status_code,
                    body=raw_body,
                    url=url,
                )
            )
        yield from self._stream_chunks_from_text(raw_body)

    def _stream_chunks_from_text(self, raw_body: str):
        event_name: str | None = None
        data_lines: list[str] = []
        saw_sse = False

        def emit_chunk():
            raw_payload = "\n".join(data_lines)
            if raw_payload.strip() == "[DONE]":
                return None
            parsed = json.loads(raw_payload) if raw_payload else {}
            if not isinstance(parsed, dict):
                raise RuntimeError("provider stream response must contain JSON object payloads")
            return JSONHTTPStreamChunk(
                event=event_name,
                payload={str(key): value for key, value in parsed.items()},
            )

        for line in raw_body.splitlines():
            if not line:
                if not data_lines:
                    event_name = None
                    continue
                chunk = emit_chunk()
                data_lines = []
                event_name = None
                if chunk is None:
                    return
                yield chunk
                continue
            if line.startswith("event:"):
                saw_sse = True
                event_name = line[6:].strip() or None
                continue
            if line.startswith("data:"):
                saw_sse = True
                data_lines.append(line[5:].lstrip())
        if data_lines:
            chunk = emit_chunk()
            if chunk is not None:
                yield chunk
            return
        if not saw_sse and raw_body.strip():
            parsed = json.loads(raw_body)
            if not isinstance(parsed, dict):
                raise RuntimeError("provider stream response must be a JSON object or SSE stream")
            yield JSONHTTPStreamChunk(
                event=None,
                payload={str(key): value for key, value in parsed.items()},
            )

    def post_json_stream(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
    ):
        body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        request_headers = dict(headers)
        request_headers.setdefault("Content-Type", "application/json")
        request_headers.setdefault("Accept", "text/event-stream")
        http_request = request.Request(
            url,
            data=body,
            headers=request_headers,
            method="POST",
        )
        try:
            with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                event_name: str | None = None
                data_lines: list[str] = []
                for raw_line in response:
                    line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
                    if not line:
                        if not data_lines:
                            event_name = None
                            continue
                        raw_payload = "\n".join(data_lines)
                        data_lines = []
                        if raw_payload.strip() == "[DONE]":
                            return
                        parsed = json.loads(raw_payload) if raw_payload else {}
                        if isinstance(parsed, dict):
                            yield JSONHTTPStreamChunk(
                                event=event_name,
                                payload={str(key): value for key, value in parsed.items()},
                            )
                        event_name = None
                        continue
                    if line.startswith("event:"):
                        event_name = line[6:].strip() or None
                        continue
                    if line.startswith("data:"):
                        data_lines.append(line[5:].lstrip())
        except error.HTTPError as exc:  # pragma: no cover - exercised by callers
            message = self._error_message(exc, url=url)
            raise RuntimeError(message) from exc
        except error.URLError as exc:  # pragma: no cover - exercised by callers
            if self._should_retry_with_curl(exc):
                yield from self._post_json_stream_with_curl(
                    url=url,
                    headers=request_headers,
                    body=body,
                )
                return
            raise RuntimeError(f"provider request failed for {url}: {exc.reason}") from exc
